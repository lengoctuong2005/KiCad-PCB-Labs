idf_component_register(SRCS "main.c"
                       INCLUDE_DIRS "."
                       REQUIRES freertos driver esp_timer esp_wifi esp_event nvs_flash lwip)
