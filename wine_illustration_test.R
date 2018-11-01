# Read data
library(gdata)
full_dataset <- read.xls("USDA Certified (Wine) 2018.10.04.xlsx", 
                         check.names = FALSE, na.strings = c("", "NA"))


# Fix dates
library(lubridate)

full_dataset$`Effective Date of CROPS Status` <- 
  as.Date(full_dataset$`Effective Date of CROPS Status`, format = "%m/%d/%Y")

full_dataset$`Effective Date of HANDLING Status` <- 
  as.Date(full_dataset$`Effective Date of HANDLING Status`, format = "%m/%d/%Y")


# Select relevant columns
names(full_dataset)
map_data <- full_dataset[c(-1, -2) ,c(5, 4, 1, 6, 13, 14, 15, 28, 29, 30)]
rownames(map_data) <- NULL
names(map_data)
names(map_data) <- c("Name", "ID", "Certifier", "Former_names", "Crops_certification", 
                     "Crops_date", "Crops", "Handling_certification",  
                     "Handling_date", "Handling_products")


# Fix factors
map_data$Crops_certification <- droplevels(map_data$Crops_certification)
map_data$Handling_certification <- droplevels(map_data$Handling_certification)
map_data$Crops <- as.character(map_data$Crops)
map_data$Handling_products <- as.character(map_data$Handling_products)
map_data$Name <- as.character(map_data$Name)
map_data$Former_names <- as.character(map_data$Former_names)


# Check vineyards/wineries that lost certification
not_certified <- c("Surrendered", "Suspended", "Revoked")
certification_status <- cbind(map_data$Name, 
                              !(map_data$Crops_certification %in% not_certified | 
                                  map_data$Handling_certification %in% not_certified))
certification_status
# Visual inspection shows that Mcclone Ranch is surrendered certification for handling, but still grows
# organic grapes for wine. Date of certification and data surrendered not apparent for data. We will 
# set "handling" variable to NA to exclude Mcclone Ranch from wineries list.
map_data[146, c('Handling_certification', 'Handling_date')]
map_data[146, c('Handling_certification', 'Handling_date')] <- NA
map_data[146, c('Handling_certification', 'Handling_date')]


# Check name changes
library(stringr)
patterns <- ("(?<=^Formerly\\s).+|(?<=^FORMERLY[:\\s+]).+|(?<=^Previously\\s).+")
Former_names_clean <- str_extract(map_data$Former_names, patterns)
Former_names_clean <- str_remove(Former_names_clean, pattern = ";\\sChanged.+")
Former_names_clean <- str_remove(Former_names_clean, pattern = "Know\\sAs\\s")
Former_names_clean


