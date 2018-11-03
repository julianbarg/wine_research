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
map_data <- full_dataset[c(-1, -2) ,c(5, 4, 1, 6, 13, 14, 15, 28, 29, 30, 39, 41, 44)]
rownames(map_data) <- NULL
names(map_data)
names(map_data) <- c("Name", "ID", "Certifier", "Former_names", "Crops_certification", 
                     "Crops_date", "Crops", "Handling_certification",  
                     "Handling_date", "Handling_products", "Address", 
                     "City", "ZIP_Code")


# Fix factors
map_data$Crops_certification <- droplevels(map_data$Crops_certification)
map_data$Handling_certification <- droplevels(map_data$Handling_certification)
map_data$Crops <- as.character(map_data$Crops)
map_data$Handling_products <- as.character(map_data$Handling_products)
map_data$Name <- as.character(map_data$Name)
map_data$Former_names <- as.character(map_data$Former_names)
map_data$Address <- as.character(map_data$Address)
map_data$City <- as.character(map_data$City)


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
Former_names_clean <- str_remove(map_data$Former_names, ".+\\(Former\\sOperation\\sID\\)$")
Former_names_clean[Former_names_clean==""] <- NA
Former_names_clean <- str_remove(Former_names_clean, "(^Formerly)")
Former_names_clean <- str_remove(Former_names_clean, "(^FORMERLY)")
Former_names_clean <- str_remove(Former_names_clean, "(^Previously)")
Former_names_clean <- str_remove(Former_names_clean, pattern = ";\\sChanged.+")
Former_names_clean <- str_remove(Former_names_clean, pattern = "\\sKnow\\sAs\\s")
Former_names_clean <- str_remove(Former_names_clean, pattern = "(^:?)")
Former_names_clean <- str_remove(Former_names_clean, pattern = "(^\\s?)")
Former_names_clean <- str_remove(Former_names_clean, pattern = "(\\s$)?")
map_data$Former_names <- Former_names_clean


# Finding matches. This algorythm only works when there is one match, 
# but could be extended to work with multiple matches.
matches <- data.frame()
i = 1
# 1: We loop over the names and see if any of them is included in any of the entries for former names.
for (name in map_data$Name) {
    match <- str_which(map_data$Former_names, name)
    matches <- rbind(matches, c(i, ifelse(length(match) == 0, NA, match)))
    i = i + 1
}
names(matches) <- c("Index", "Match")
# As a result, we have a dataframe with the index of every entry of former names for which there is a match.
# Some match with themselves. Visual inspection shows that these name changes do not have any effect on the 
# data we care about (date of certification). Therefore, we override those matches with NA.
self_match <- (matches$Index == matches$Match)
self_match[is.na(self_match)] <- TRUE
matches$Match[self_match] <- NA

# Clean the map data accordingly
matches <- matches[!is.na(matches$Match), ]
for (row  in 1:nrow(matches)){
  Match <- matches$Match[row]
  Index <- matches$Index[row]
  if (!is.na(map_data$Crops_date[Index]) &!is.na(map_data$Crops_date[Match]) &
      (map_data$Crops_date[Index] < map_data$Crops_date[Match]))
    map_data$Crops_date[Match] <- map_data$Crops_date[Index]
      
  if (!is.na(map_data$Handling_date[Index]) &!is.na(map_data$Handling_date[Match]) &
      (map_data$Handling_date[Index] < map_data$Handling_date[Match]))
    map_data$Handling_date[Match] <- map_data$Handling_date[Index]
}
map_data <- map_data[-(matches$Index), ]


# Remove accidental missmatched (e.g, for farms that produce wine and apples, we remove
# the "Crops" column)
not_vineyard <- !str_detect(map_data$Crops, pattern = ("grape|Grape|wine|Wine"))
not_vineyard[is.na(not_vineyard)] <- FALSE
# not_vineyard
not_winery <- !str_detect(map_data$Handling_products, pattern = ("wine|Wine"))
not_winery[is.na(not_winery)] <- FALSE
# not_winery
map_data[not_vineyard, c("Crops_certification", "Crops_date", "Crops")] <- NA
map_data[not_winery, c("Handling_certification", "Handling_date", "Handling_products")] <- NA

saveRDS(map_data, file = "map_data.rds")
