process <- function(filename) {
  # Read the file line by line.
  conn <- file(filename, open='r')
  lines <-readLines(conn)
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