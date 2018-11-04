#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(ggplot2)
library(ggmap)
library(lubridate)

load("roadmap.RData")
load("toner_lite.RData")
load("final_loc.RData")
load("toner_lines.RData")

calculateVineyardWinery <- function(year, df=final_loc) {
  # Calculate the status of an organization in the selected year
  library(lubridate)
  crops_years <- interval(final_loc$Crops_date, date_decimal(2018))
  vineyard <- (date_decimal(year) %within% crops_years)
  handling_years <- interval(final_loc$Handling_date, date_decimal(2018))
  winery <- (date_decimal(year) %within% handling_years)
  
  Type <- NA
  Type <- ifelse(vineyard %in% TRUE, "Vineyard", Type)
  Type <- ifelse(winery %in% TRUE, "Winery", Type)
  Type <- ifelse((vineyard %in% TRUE) & (winery %in% TRUE), "Vineyard & Winery", Type)
  df <- cbind(df, Type = ordered(Type, levels = c("Vineyard", "Winery", "Vineyard & Winery")))
}


# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
     sidebarPanel(
       h2("Organic Vineyards and Wineries in CA"),
       tabsetPanel(
         tabPanel("Selections",
                  checkboxGroupInput("type",
                                     "Show:",
                                     c("Vineyard", "Winery", "Vineyard & Winery"),
                                     selected = c("Vineyard", "Winery", "Vineyard & Winery")),
                  sliderInput("year",
                              "Year:",
                              min = 2000, 
                              max = 2018,
                              step = 1,
                              sep = "",
                              ticks = FALSE,
                              value = 2010),
                  radioButtons("type", 
                               "Organic or biodynamic:",
                               c("Organic", "Biodynamic", "Both"),
                               selected = "Both"),
                  selectInput("style",
                              "Map style:",
                              choices = c("roadmap", "toner_lite", "toner_lines"),
                              selected = "Toner-lines")
                  ),
         
         tabPanel("Plotting Options",
                  checkboxInput("plot_onoff",
                                "Show datapoints",
                                TRUE),
                  checkboxInput("rug",
                                "Show rug",
                                FALSE),
                  checkboxInput("density_onoff",
                                "Show density",
                                FALSE),
                  selectInput("shape",
                              "Shape indicates:",
                              choices = c("Vineyard/Winery", "Certifier", "Organic/Biodynamic"),
                              selected = "Vineyard/Winery"),
                  sliderInput("size",
                              "Size of data points:",
                              min = 1,
                              max = 10,
                              ticks = FALSE,
                              value = 3),
                  sliderInput("transparency",
                              "Transparency:",
                              min = 0.1,
                              max = 1,
                              step = 0.1,
                              ticks = FALSE,
                              value = 0.6),
                  sliderInput("jitter",
                              "Jitter - zero means no jitter:",
                              min = 0,
                              max = 0.15,
                              step = 0.01,
                              ticks = FALSE,
                              value = 0)
                  ),
                 
         
         tabPanel("Certifiers",
                  checkboxGroupInput("certifiers",
                                     "",
                                     levels(final_loc$Certifier),
                                     selected = levels(final_loc$Certifier)
                                     )
                  )
         )
       ),
     mainPanel(plotOutput(outputId = "map")
               # DT::dataTableOutput("display_table")
               )
     )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  filter_df <- reactive({
    req(input$year)
    req(input$type)
    req(input$certifiers)
    filter_year <- calculateVineyardWinery(input$year, final_loc)
    filter_type <- filter_year[filter_year$Type %in% input$type,]
    filter_cert <- filter_type[filter_type$Certifier %in% input$certifiers, ]
    # Reordering the factor variable Certifier after creating our selection
    # allows us to use the shapes argument on it in our map without worrying that
    # there are not enough shapes with both fill and color to make an interpretable map.
    # Some datapoints may not have fill and color, but there will not be a lot of them.
    # The most frequent ones will have both fill and color.
    filter_cert$Certifier <- reorder(filter_cert$Certifier, 
                                     filter_cert$Certifier, 
                                     FUN=function(x) -length(x))
    filter_cert
  })
  
  shape_argument <- reactive({
    if (input$shape == "Certifier"){"Certifier"}
    else if (input$shape == "Organic/Biodynamic"){"Certifier"}
    else if (input$shape == "Vineyard/Winery"){"Type"}
  })
  
  output$map <- renderPlot({
    library(ggplot2)
    library(ggmap)
    req(input$shape)
    req(input$size)
    req(input$transparency)
    req(input$style)
    map <- ggmap(get(input$style), base_layer = ggplot(filter_df(), aes(lon, lat))) +
      scale_shape_manual(values = c(21:25,1:20), name = shape_argument()) +
      scale_color_brewer(palette = "Set1")
      # scale_color_discrete()
      # scale_color_manual(values=c("#999999", "#E69F00", "#56B4E9"))
    
    if (input$plot_onoff) {
      map <- map + geom_point(aes(shape = get(shape_argument()), fill = Type), 
                 size = input$size, 
                 alpha = input$transparency,
                 # pch = 21,
                 color = "black",
                 position = position_jitter(width = input$jitter, 
                                            height = input$jitter))
    }
    
    if (input$rug) {
      map <- map + geom_rug(alpha = 0.2)
    }
    
    if (input$density_onoff) {
      map <- map +
        geom_density2d()
    }
    
    map
    
  }, width = 800, height = 800)
  
  # 
  # output$display_table <- DT::renderDataTable({
  #   DT::datatable(data = filter_df(),
  #                 options = list(pageLength = 10),
  #                 rownames = FALSE)
  # })
}

# Run the application 
shinyApp(ui = ui, server = server)

