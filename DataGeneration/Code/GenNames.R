##########################################################
# PROJECT: Never Audit Again - Fake Name Generation      #
# AUTHORS: Colin Sullivan                                #
# DATE CREATED: 3/10/2016                                #
# DATE EDITED:                                           #
# NOTES:                                                 #
##########################################################

########################################################
#    INITIALIZATION
########################################################
  rm(list = ls())  
  
  # Set Working Directories: 
  work <- 'C:/Users/colin/Dropbox/Resume-audit/Scraping Project/Data Sources/Names/GeneratedData'
  home <- '/Users/colin/Dropbox/Resume-audit/Scraping Project/Data Sources/Names/GeneratedData'
  output <- ''
  setwd(home) ### Set user here ###  
  
  # Load Libraries, set seed
  set.seed(19104)
  imwidth <- 6
  imheight <- 3.7

########################################################
#    Generate Names
########################################################
  sampsize <- 50 
  proper=function(x) paste0(toupper(substr(x, 1, 1)), tolower(substring(x, 2)))

  ### White names
  wm.fn <- as.vector(read.csv('fn_whitemales.csv')[,'BFNAME'])
  wf.fn <- as.vector(read.csv('fn_whitefemales.csv')[,'BFNAME'])
  w.ln <- as.vector(read.csv('ln_white.csv')[,'name'])
  w.ln <- w.ln[!is.na(w.ln)]
  wm.ln.samp <- sample(w.ln, sampsize)  
  wm.fn.samp <- sample(wm.fn, sampsize)  
  
  wf.fn.samp <- sample(wf.fn, sampsize)  
  wf.ln.samp <- sample(w.ln, sampsize)  
  
  white.male.sample <- paste(proper(wm.fn.samp), proper(wm.ln.samp))
  white.female.sample <- paste(proper(wf.fn.samp), proper(wf.ln.samp))

  write.table(white.female.sample, paste(output, 'white_fem_sample.csv', sep=""), sep=',', row.names=FALSE, col.names=c('Name'))
  write.table(white.male.sample, paste(output, 'white_male_sample.csv', sep=""), sep=',', row.names=FALSE, col.names=c('Name'))

  ### Black names
  bm.fn <- as.vector(read.csv('fn_blackmales.csv')[,'BFNAME'])
  bf.fn <- as.vector(read.csv('fn_blackfemales.csv')[,'BFNAME'])
  b.ln <- as.vector(read.csv('ln_black.csv')[,'name'])
  bm.ln.samp <- sample(b.ln, sampsize)  
  bm.fn.samp <- sample(bm.fn, sampsize)  
  
  bf.fn.samp <- sample(bf.fn, sampsize)  
  bf.ln.samp <- sample(b.ln, sampsize)  

  black.male.sample <- paste(proper(bm.fn.samp), proper(bm.ln.samp))
  black.female.sample <- paste(proper(bf.fn.samp), proper(bf.ln.samp))

  write.table(black.female.sample, paste(output, 'black_fem_sample.csv', sep=""), sep=',', row.names=FALSE, col.names=c('Name'))
  write.table(black.male.sample, paste(output, 'black_male_sample.csv', sep=""), sep=',', row.names=FALSE, col.names=c('Name'))

  ### Asian names
  am.fn <- as.vector(read.csv('fn_asianmales.csv')[,'BFNAME'])
  af.fn <- as.vector(read.csv('fn_asianfemales.csv')[,'BFNAME'])
  a.ln <- as.vector(read.csv('ln_asian.csv')[,'name'])
  am.ln.samp <- sample(a.ln, sampsize)  
  am.fn.samp <- sample(am.fn, sampsize)  
  
  af.fn.samp <- sample(af.fn, sampsize)  
  af.ln.samp <- sample(a.ln, sampsize)  
  
  asian.male.sample <- paste(proper(am.fn.samp), proper(am.ln.samp))
  asian.female.sample <- paste(proper(af.fn.samp), proper(af.ln.samp))

  write.table(asian.female.sample, paste(output, 'asian_fem_sample.csv', sep=""), sep=',', row.names=FALSE, col.names=c('Name'))
  write.table(asian.male.sample, paste(output, 'asian_male_sample.csv', sep=""), sep=',', row.names=FALSE, col.names=c('Name'))

  ### Hispanic names
  hm.fn <- as.vector(read.csv('fn_hispanicmales.csv')[,'BFNAME'])
  hf.fn <- as.vector(read.csv('fn_hispanicfemales.csv')[,'BFNAME'])
  h.ln <- as.vector(read.csv('ln_hispanic.csv')[,'name'])
  
  hm.ln.samp <- sample(h.ln, sampsize)  
  hm.fn.samp <- sample(hm.fn, sampsize)  
  
  hf.fn.samp <- sample(hf.fn, sampsize)  
  hf.ln.samp <- sample(h.ln, sampsize)  
  
  hispanic.male.sample <- paste(proper(hm.fn.samp), proper(hm.ln.samp))
  hispanic.female.sample <- paste(proper(hf.fn.samp), proper(hf.ln.samp))

  write.table(hispanic.female.sample, paste(output, 'hispanic_fem_sample.csv', sep=""), sep=',', row.names=FALSE, col.names=c('Name'))
  write.table(hispanic.male.sample, paste(output, 'hispanic_male_sample.csv', sep=""), sep=',', row.names=FALSE, col.names=c('Name'))
