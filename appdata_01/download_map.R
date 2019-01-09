map_data <- readRDS("map_data.rds")


# Load latest version of ggmap from github (should already be taken care of)
if(!requireNamespace("devtools")) install.packages("devtools")
devtools::install_github("dkahle/ggmap", ref = "tidyup")


# Prepare ggmap (loag google key)
library(ggplot2)
library(ggmap)
key <- readChar('maps_key.txt', file.info('maps_key.txt')$size)
register_google(key = key)

 
# Load and inspect map
roadmap <- get_map("California", zoom = 6, source = "google", 
                      maptype = "roadmap")  # Using Google Maps.
toner_lite <- get_map("California", zoom = 6, source = "google", 
                       maptype = "toner-lite") # Using Stamen.
toner_lines <- get_map("California", zoom = 6, source = "google", 
                       maptype = "toner-lines")
ggmap(roadmap)
ggmap(toner_lite)


# Get coordinates of vineyards/wineries
library(dplyr) 
map_loc <- map_data %>%
  mutate(loc = paste0(Address, ", ", City, ", CA")) %>%
  mutate_geocode(location = loc)


# Add locations that were not found
missing <- map_loc %>%
  filter(is.na(lon)) %>%
  select(-one_of(c("loc", "lon", "lat"))) %>%
  mutate(loc = paste(ZIP_Code, City, "CA")) %>%
  mutate_geocode(loc)
map_loc$lon <- ifelse(is.na(map_loc$lon), missing$lon[missing$Name %in% map_loc$Name], map_loc$lon)
map_loc$lat <- ifelse(is.na(map_loc$lat), missing$lat[missing$Name %in% map_loc$Name], map_loc$lat)


# Added droplevels here & in preprocessing, could be removed here.
map_loc$Certifier <- droplevels(map_loc$Certifier)
final_loc <- map_loc[ ,c(-4, -5, -8)]


# Export
# saveRDS(roadmap, file = "roadmap.rds")
# saveRDS(toner_lite, file = "toner_lite.rds")
# saveRDS(final_loc, file = "final_loc.rds")
# saveRDS(roadmap, file = "wine_illustration/roadmap.rds")
# saveRDS(toner_lite, file = "wine_illustration/toner_lite.rds")
# saveRDS(final_loc, file = "wine_illustration/final_loc.rds")
save(roadmap, file = "roadmap.RData")
save(toner_lite, file = "toner_lite.RData")
save(final_loc, file = "final_loc.RData")
save(toner_lines, file = "toner_lines.RData")
save(roadmap, file = "wine_illustration/roadmap.RData")
save(toner_lite, file = "wine_illustration/toner_lite.RData")
save(final_loc, file = "wine_illustration/final_loc.RData")
save(toner_lines, file = "wine_illustration/toner_lines.RData")
