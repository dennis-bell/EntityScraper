# EntityScraper Add-on for Home Assistant

The `EntityScraper` add-on for Home Assistant provides a seamless way to monitor and track the availability and unavailability of entities. It logs these states into a SQLite database, allowing users to gain insights into the uptime and downtime of their devices and integrations.

## 🚀 Features:

- **Entity State Monitoring**: Automatically tracks when an entity becomes unavailable.
- **Persistence**: Logs unavailable states to a SQLite database.
- **Exponential Backoff**: Implements an exponential backoff mechanism in case of disconnection, ensuring optimized reconnection attempts.
- **Integration with Home Assistant**: Exposes data back to Home Assistant, allowing users to check how long, in hours, entities have been unavailable.

## 📦 Installation:

1. Navigate to **Supervisor > Add-on Store** in Home Assistant.
2. Use the menu in the upper-right corner to add this repository: 
https://github.com/dennis-bell/EntityScraper
3. Look for the `EntityScraper` add-on in the list and install it.

## ⚙️ Configuration:

(Provide any necessary configuration steps, if applicable. For instance, if users need to provide database paths, or set any specific settings before starting the add-on.)

## 🔧 Usage:

1. After installation and necessary configurations, start the `EntityScraper` add-on.
2. Monitor entity availability using the exposed integration in Home Assistant.

## 🛠 Support & Contribution:

For any issues, questions, or suggestions, please open an issue on the [GitHub repository](https://github.com/dennis-bell/EntityScraper/issues).

Contributions to improve or enhance the `EntityScraper` add-on are always welcome. Please fork the repository and create a pull request with your changes.
