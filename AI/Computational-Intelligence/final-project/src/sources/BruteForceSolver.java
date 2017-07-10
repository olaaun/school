package sources;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

/*
 * Solves the problem with bruteforce method
 * I.e. trying every possible route
 * Used for comparison of genetic algorithm result
 */
public class BruteForceSolver {

	//Return a list of all cities in the cities-list,
	//except origin and destination of traveler
	private static List<Integer> getVisitList(Traveller trv, List<City> cities) {
		List<Integer> visitList = IntStream.range(0, cities.size()).boxed().collect(Collectors.toList());
		visitList.remove(Arrays.asList(trv.origin, trv.destination));
		return visitList;
	}

	//Recursive function, which will return a list
	//containing every permutation of function parameter
	private static List<List<Integer>> getPermutations(List<Integer> list) {
		List<List<Integer>> allPermutations = new ArrayList<>();
		if (list.size() == 0) {
			allPermutations.add(new ArrayList<>());
			return allPermutations;
		}
		int firstElement = list.remove(0);
		List<List<Integer>> permutations = getPermutations(list);
		for (List<Integer> occ : permutations) {
			for (int index = 0; index <= occ.size(); index++) {
				List<Integer> temp = new ArrayList<>(occ);
				temp.add(index, firstElement);
				allPermutations.add(temp);
			}
		}
		return allPermutations;

	}

	public static void main(String[] args) {
		List<City> cities = new CityGenerator().generateCityList();
		for(City city: cities) {
			System.out.println(city.name);
		}
		List<Traveller> travellers = new ArrayList<>();

		//Find indices of destination and origin points
		int taipei = cities.indexOf(new City("Taipei", -1, -1));
		int surabaya = cities.indexOf(new City("Surabaya", -1, -1));
		int paris = cities.indexOf(new City("Paris", -1, -1));
		int banjul = cities.indexOf(new City("Banjul", -1, -1));
		int oslo = cities.indexOf(new City("Oslo", -1, -1));

		travellers.add(new Traveller(surabaya, taipei, new ArrayList<>()));
		travellers.add(new Traveller(paris, taipei, new ArrayList<>()));
		travellers.add(new Traveller(banjul, taipei, new ArrayList<>()));
		travellers.add(new Traveller(oslo, taipei, new ArrayList<>()));

		/*
		 * For every traveler, get every possible route
		 * and save the shortest one
		 */
		for (Traveller trv : travellers) {
			//Creates the list of transit points between origin and destination
			//Then gets every permutation of that list
			List<Integer> citiesToVisit = getVisitList(trv, cities);
			List<List<Integer>> allPermutations = getPermutations(citiesToVisit);

			double currentBest = Double.MAX_VALUE;
			List<Integer> bestOrder = null;
			for (List<Integer> permutation : allPermutations) {
				trv.orderVisit = permutation;
				double totalCost = trv.totalCostTravel(cities);
				if (totalCost < currentBest) {
					currentBest = totalCost;
					bestOrder = permutation;
				}
			}
			String order = "";
			for (Integer index : bestOrder) {
				order += cities.get(index).name + ",";
			}
			System.out.println(currentBest + "   " + order.substring(0, order.length() - 1));
		}

	}

}
