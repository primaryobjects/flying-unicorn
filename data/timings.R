#
# Analytics program to produce timing metrics for running a quantum computing program
# on a QisKit simulator versus IBM Q Experience.
# The metrics include: machine name | min seconds | mean seconds | max seconds
# The results show significant wait times for programs executed on IBM Q Experience versus the simulator.
#
# Kory Becker, 2019
# http://primaryobjects.com
#

process <- function(filename) {
  # Read the file line by line.
  conn <- file(filename, open='r')
  lines <-readLines(conn, warn=F)
  close(conn)

  # Extract the lines with timing information.
  timings <- lines[grep('Request completed in (\\d+\\.\\d+)m (\\d+\\.\\d+)s', lines)]
  machines <- lines[grep('Running on (\\w+)', lines)]

  # Create a tidy dataset with the original text, machine name, and timing metrics.
  logs <- sapply(seq_along(timings), function(i) {
    line <- timings[i]
    machine <- machines[i]
    matches <- unlist(regmatches(line, regexec('(\\d+\\.\\d+)m (\\d+\\.\\d+)s', line)))
    matches2 <- unlist(regmatches(machine, regexec('Running on (\\w+)', machine)))
    c(text=line, machine=matches2[2], minutes=as.numeric(matches[2]), seconds=as.numeric(matches[3]), total=(as.numeric(matches[2])*60) + as.numeric(matches[3]))
  })

  # Convert to a data frame.
  data <- as.data.frame(t(logs), stringsAsFactors=F)

  # Format the column types.
  data[,2] <- as.factor(data[,2])
  data[,3] <- as.numeric(data[,3])
  data[,4] <- as.numeric(data[,4])
  data[,5] <- as.numeric(data[,5])

  # Save the tidy dataset.
  write.csv(data, file=gsub('\\.\\w{3}', '\\.csv', filename))

  data
}

data <- process('timings.txt')
dataSim <- process('timings-sim.txt')
data2 <- process('timings-ibmqx4.txt')

# Split the data-set by machine name.
ibmq <- rev(split(data, data$machine))

# Create a summary table of machine name, min, mean, and max metrics.
summary <- data.frame(
  type=c(as.character(dataSim$machine[1]), names(ibmq[1])[1], names(ibmq[2])[1], 'IBM Q Experience'),
  runs=c(length(dataSim$text), length(ibmq[[1]]$text), length(ibmq[[2]]$text), nrow(data)),
  min=c(min(dataSim$total), min(ibmq[[1]]$total), min(ibmq[[2]]$total), min(data$total)),
  mean=c(mean(dataSim$total), mean(ibmq[[1]]$total), mean(ibmq[[2]]$total), mean(data$total)),
  max=c(max(dataSim$total), max(ibmq[[1]]$total), max(ibmq[[2]]$total), max(data$total))
)
print(summary)
