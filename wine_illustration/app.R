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


# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("Organic Vineyards and Wineries in CA"),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
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
                                selected = "Both")
                   ),
          
          tabPanel("Plot Options",
                   selectInput("shape",
                               "Shape indicates:",
                               choices = c("Certifier", "Organic/Biodynamic", "Vineyard/Winery"),
                               selected = "Certifier"),
                   sliderInput("size",
                               "Size of data points:",
                               min = 1,
                               max = 10,
                               ticks = FALSE,
                               value = 2),
                   sliderInput("transparency",
                               "Transparency:",
                               min = 0.1,
                               max = 1,
                               step = 0.1,
                               ticks = FALSE,
                               value = 0.3),
                   selectInput("style",
                               "Style:",
                               choices = c("roadmap", "toner_lite"),
                               selected = "Toner-lite")
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
      mainPanel(h3("Test"),
                DT::dataTableOutput("display_table")
                )
      )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  # 
  # winery <- reactive({
  #   req(input$year)
  #   crops_years <- interval(final_loc$Crops_date, date_decimal(2018))
  #   vineyard <- (date_decimal(input$year)) %within% crops_years
  # })
  # 
  # vineyard <- reactive({
  #   req(input$year)
  #   handling_years <- interval(final_loc$Handling_date, date_decimal(2018))
  #   winery <- (date_decimal(input$year)) %within% crops_years
  # })
  
  filter_year <- reactive({
    req(input$year)
    crops_years <- interval(final_loc$Crops_date, date_decimal(2018))
    vineyard <- (date_decimal(input$year)) %within% crops_years
    handling_years <- interval(final_loc$Handling_date, date_decimal(2018))
    winery <- (date_decimal(input$year)) %within% crops_years
    cbind(vineyard, winery)
  })

  output$display_table <- DT::renderDataTable({
    DT::datatable(data = filter_year(),
                  options = list(pageLength = 3),
                  rownames = FALSE)
  })
}

# Run the application 
shinyApp(ui = ui, server = server)

