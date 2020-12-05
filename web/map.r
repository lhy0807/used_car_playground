library(leaflet)
library(rgdal)
library(sf)
library(htmltools)
library(htmlwidgets)

USA_data <- st_read("map2/USA_data.shp")


pal <- colorFactor(
  palette = c('#fff5f0', '#b4b4b4', '#fb6a4a', '#fcbba1'),
  domain = US$category
)


USA_data$label <- paste("<p><b>", USA_data$NAME, "</b></p>",
                  "Category: ", USA_data$category, "<br>",
                  "Percent Change From 2016-2017: ", USA_data$change, "<br>",
                  "Statistically ignificant: ",USA_data$significan, "<br>",
                  "2016 Number: ", USA_data$X2016number, "<br>",
                  "2016 Rate: ", USA_data$X2016rate, "<br>",
                  "2017 Number: ", USA_data$X2017number, "<br>",
                  "2017 Rate: ", USA_data$X2017rate)

my_map <- leaflet(USA_data) %>%
  addPolygons(color = "#444444", weight = 1, smoothFactor = 0.5,
              opacity = 1.0, fillOpacity = 0.5,
              fillColor = ~pal(category),
              highlightOptions = highlightOptions(color = "white", weight = 2,
                                                  bringToFront = TRUE),
              label=lapply(USA_data$label, HTML),
              labelOptions = labelOptions(textsize = "15px")) %>%
  addLegend(position="bottomright", pal=pal, values=~category, title="Category", opacity=1) %>%
  setView(lng=-98.134, lat=38.053, zoom=4)
saveWidget(widget=my_map, file="my_map.html")


library(shiny)
library(ggplot2)

ui <- shinyUI(fluidPage(
  headerPanel(title = 'Test Kmeans'),
  sidebarPanel(
    selectInput(inputId = 'Col',label = 'The Variables',
                choices = c('Sepal.Length','Sepal.Width','Petal.Length','Petal.Width'),
                selected = c('Sepal.Length','Sepal.Width'),
                multiple = T),
    numericInput(inputId = 'center',label = 'Centroids',value = 3,min = 1,max = 10,step = 1),
    submitButton(text='submit')
  ),
  mainPanel(
    h1('The result of Kmeans'),
    plotOutput(outputId = 'plot')
  )
))


server <- shinyServer(function(input,output){
  output$plot <- renderPlot({
    da <- iris[,input$Col]
    fit <- kmeans(da,centers = input$center)
    da$cluster <- fit$cluster
    da2 <- as.data.frame(fit$centers)
    ggplot()+
      geom_point(data = da,aes(x=da[,input$Col[1]],y=da[,input$Col[2]],color=factor(cluster)))+
      geom_point(data = da2,aes(x=da2[,names(da2)[1]],y=da2[,names(da2)[2]],color=factor(1:nrow(da2))),size=5,shape=3)+
      xlab(input$Col[1])+ylab(input$Col[2])
    })
})

outline <- quakes[chull(quakes$long, quakes$lat),]

map <- leaflet(quakes) %>%
  # Base groups
  addTiles(group = "OSM (default)") %>%
  addProviderTiles(providers$Stamen.Toner, group = "Toner") %>%
  addProviderTiles(providers$Stamen.TonerLite, group = "Toner Lite") %>%
  # Overlay groups
  addCircles(~long, ~lat, ~10^mag/5, stroke = F, group = "Quakes") %>%
  addPolygons(data = outline, lng = ~long, lat = ~lat,
    fill = F, weight = 2, color = "#FFFFCC", group = "Outline") %>%
  # Layers control
  addLayersControl(
    baseGroups = c("OSM (default)", "Toner", "Toner Lite"),
    overlayGroups = c("Quakes", "Outline"),
    options = layersControlOptions(collapsed = FALSE)
  )


/////////////////
ui <- shinyUI(fluidPage(


   absolutePanel(width = 430,top=200,left = 'auto',draggable = T,
                 textInput(inputId = 'Loc',label = 'THE PLACE'),
                 textInput(inputId = 'Start',label = 'FROM',width = "50%"),
                 textInput(inputId = 'End',label = 'TO',width = "50%"),
                 selectInput(inputId = 'selected',label = 'Route or Loc',
                             choices = c('Loc','Route'),selected = 'Loc',
                             multiple = F),
                 textOutput(outputId = 'Request'),
                 submitButton(text = "Submit")
                 )
))

server <- shinyServer(function(input, output) {

    ## acquire the coordinate from rjson file
    getcoord <- function(x){## x is a name of some place
      x <- fromJSON(getCoordinate(x))
      return(x)
    }

    ## output leaflet map to the id:map
    output$map <- renderLeaflet({
      m <- leaflet()
      m <- m%>%addTiles()

      if(input$selected == 'Loc'){
        temp <- getcoord(input$Loc)
        if(temp$status!=0){
          output$Request <- renderText({
            c('The location failed to be found')
          })
          m
        }else{
          output$Request <- renderText({
            c('The location is found successfully')
          })
          m %>% addMarkers(lng=temp$result$location$lng,
                          lat=temp$result$location$lat,
                          popup = paste0(input$Loc,'--',temp$result$level))
        }
      }else{
        temp1 <- getcoord(input$Start)
        temp2 <- getcoord(input$End)
        if(temp1$status==0&temp2$status==0){
          output$Request <- renderText({
            c('Both start point and end point are valid')
          })
          route <- getRoute(input$Start,input$End)
          m%>%addPolylines(route$lon,route$lat)%>%
            addMarkers(lng=route$lon[c(1,nrow(route))],
                      lat=route$lat[c(1,nrow(route))],
                            popup = c(paste0(input$Start,'--',temp1$result$level),
                                      paste0(input$End,'--',temp2$result$level)))
        }else{
            output$Request <- renderText({
              c('One or both of origin and destination is invalid')
            })
          }
        }
    })
})


server <- function(input, output, session) {
  filteredData <- reactive({
    df_history[df_history$years >= input$range[1] & df_history$years <= input$range[2],]
  })
  
  output$map <- renderLeaflet({
    leaflet(df_history) %>% addTiles() %>%
      fitBounds(~min(lng), ~min(lat), ~max(lng), ~max(lat))
  })
  
  observe({
    proxy <- leafletProxy("map", data = df_history)
    proxy %>% clearControls()
    
    if (input$legend) {
      catego <- unique(df_history$owner)
      proxy %>% addLegend(position = "bottomright", colors = RdYlBu(catego),
                          labels = catego
      )
      
      leafletProxy("map", data = filteredData()) %>%
        clearShapes() %>% clearMarkerClusters() %>%
        addCircles(weight = ~size_check,
                   color = ~RdYlBu(owner),
                   opacity = 1,
                   fillOpacity = 1)
      
    }
    else{
      leafletProxy("map", data = filteredData()) %>%
        clearShapes() %>% clearMarkerClusters() %>%
        addMarkers(popup = ~paste("<h5>",name_tw,"</h5>",
                                  years,"year<br>",
                                  address,"<br>"),
                   clusterOptions = markerClusterOptions()) # %>%
      
    }
  })
}


library(shiny)
library(leaflet)
library(RColorBrewer)
library(shinythemes)

ui <- bootstrapPage(
  theme = shinytheme("cosmo"),
  title = "Taiwan Historical Map",
  tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
  leafletOutput("map", width = "100%", height = "100%"),
  absolutePanel(top = 100, right = 30,
                draggable = FALSE,
                sliderInput("range", "Years", 1800, 2000,
                            value = c(1800,2000), step = 10
                ),
                checkboxInput("legend", "Show Scatter Diagram", FALSE)
  ),
  absolutePanel(top = 20, right = 42,
                titlePanel(h2("Taiwan Historical Map"))
  )
)

## Setup work directory;
setwd("/srv/shiny-system/Data") 
I <- 0
for (i in 1:60) {
  system("top -n 1 -b -u shiny > top.log")
  dat <- readLines("top.log")
  id <- grep("R *$", dat)
  Names <- strsplit(gsub("^ +|%|\\+", "", dat[7]), " +")[[1]]
  if (length(id) > 0) {
    # 'top' data frame;
    L <- strsplit(gsub("^ *", "", dat[id]), " +")
    dat <- data.frame(matrix(unlist(L), ncol = 12, byrow = T))
    names(dat) <- Names
    dat <- data.frame(Time = Sys.time(), dat[, -ncol(dat)], usr = NA, app = NA)
    dat$CPU <-as.numeric(as.character(dat$CPU))
    dat$MEM <-as.numeric(as.character(dat$MEM))
    # Check if connection number changed;
    for (i in 1:length(dat$PID)) {
      PID <- dat$PID[i]
      system(paste("sudo netstat -p | grep", PID, "> netstat.log"))
      system(paste("sudo netstat -p | grep", PID, ">> netstat.log2"))
      system(paste("sudo lsof -p", PID, "| grep /srv > lsof.log"))
      netstat <- readLines("netstat.log")
      lsof <- readLines("lsof.log")
      dat$usr[i] <- length(grep("ESTABLISHED", netstat) & grep("tcp", netstat))
      dat$app[i] <- regmatches(lsof, regexec("srv/(.*)", lsof))[[1]][2]
    }
    dat <- dat[, c("app", "usr")]
  } else {
    dat <- data.frame(app = "app", usr = 0)
  }
  write.table(dat, file = "CPU.txt")
}

ui <- bootstrapPage(
  
  tags$head(
    tags$link(href = "https://fonts.googleapis.com/css?family=Oswald", rel = "stylesheet"),
    tags$style(type = "text/css", "html, body {width:100%;height:100%; font-family: Oswald, sans-serif;}"),
    includeHTML("meta.html"),
    tags$script(src="https://cdnjs.cloudflare.com/ajax/libs/iframe-resizer/3.5.16/iframeResizer.contentWindow.min.js",
                type="text/javascript"),
    tags$script('
                $(document).ready(function () {
                  navigator.geolocation.getCurrentPosition(onSuccess, onError);
                
                  function onError (err) {
                    Shiny.onInputChange("geolocation", false);
                  }
                
                  function onSuccess (position) {
                    setTimeout(function () {
                      var coords = position.coords;
                      console.log(coords.latitude + ", " + coords.longitude);
                      Shiny.onInputChange("geolocation", true);
                      Shiny.onInputChange("lat", coords.latitude);
                      Shiny.onInputChange("long", coords.longitude);
                    }, 1100)
                  }
                });
                ')
  ),
  
  leafletOutput("map", width = "100%", height = "100%"),
