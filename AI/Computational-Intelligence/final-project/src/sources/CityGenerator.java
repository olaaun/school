package sources;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class CityGenerator {

	private static final String FILENAME = "airports.dat";
	private static ArrayList<City> cities = new ArrayList<>();

	// Key is city name, value is country
	// Needed when finding coordinates, to ensure correct city
	// E.g. Lima is a city in both Peru and US
	private static HashMap<String, String> cityCountry = new HashMap<>();

	public CityGenerator() {
		cityCountry.put("Paris", "France");
		cityCountry.put("Banjul", "Gambia");
		cityCountry.put("Surabaya", "Indonesia");
		cityCountry.put("Washington", "United States");
		cityCountry.put("Oslo", "Norway");
		cityCountry.put("Lima", "Peru");
		cityCountry.put("Moscow", "Russia");
		cityCountry.put("Sydney", "Australia");
		cityCountry.put("Taipei", "Taiwan");
	}

	public List<City> generateCityList() {
		try {
			FileReader fr = new FileReader(FILENAME);
			BufferedReader reader = new BufferedReader(fr);
			String line = reader.readLine();
			while (line != null) {
				String[] splitLine = line.split(",");
				String cityName = splitLine[2].replaceAll("\"", "");
				String country = splitLine[3].replaceAll("\"", "");

				if (cityCountry.containsKey(cityName) && 
						country.equals(cityCountry.get(cityName))) {

					// First element latitude, second longitude
					double lat = Double.parseDouble(splitLine[6]);
					double lng = Double.parseDouble(splitLine[7]);
					City city = new City(cityName, lat, lng);
					if (!cities.contains(city)) {
						cities.add(city);
					}

				}
				line = reader.readLine();
			}
			reader.close();
			fr.close();
		} catch (Exception e) {
			System.err.println("Something went wrong\n" + e);
		}

		return cities;
	}

}
