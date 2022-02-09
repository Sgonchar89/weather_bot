![Weather_bot workflow](https://github.com/Sgonchar89/weather_bot/actions/workflows/weather_bot_workflow.yml/badge.svg)

# Weather_outside_bot

## Description:
Telegram weather bot provides the current weather forecast for the city entered by the user. 
Functionality: 
1. The user starts the Telegram bot with the command /start 
2. The bot replies by saying it is ready to start.
3. User enters the name of the city.
4. The bot sends a weather report for the entered city
The project uses the OpenWeatherMap API, which provides current weather data, forecasts and maps with weather phenomena such as clouds, wind, pressure and precipitation. All-weather data can be retrieved in JSON, XML or HTML formats. This project uses the JSON format from which the necessary weather information is output in a message from the bot.

## Project launch
### Receiving an openweather token: 
```
https://openweathermap.org/api
```

### Receiving an Telegram token: 
1. To register a Telegram bot account, use the special bot @BotFather.
2. Click the Start button. Then command /newbot and specify parameters of the new bot:
- the name (in any language) under which your bot will appear in the list of contacts;
- the technical name of your bot, by which it will be found in Telegram. The name must end with the word bot.
3. @BotFather will send a Bot API token to the chat. The token looks something like this:

```
123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

### Cloning a project from GitHub:
```
git clone https://github.com/Sgonchar89/weather_bot
```

### Description of the .env file:
This file contains the environment variables for the Telegtam bot
```
TELEGRAM_TOKEN = "enter_your_token"
OPENWEATHER_TOKEN = "enter_your_token"
```