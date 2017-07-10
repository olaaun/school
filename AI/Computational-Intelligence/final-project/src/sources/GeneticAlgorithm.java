package sources;

import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class GeneticAlgorithm {
	// list of the cities, their index will be used by the travellers to
	// reference them(chromosoms)
	static List<City> cities = new CityGenerator().generateCityList();
	// number of chromosoms
	static int nbChrom = 100;
	// number of generations
	static int nbGener = 200;
	// crossover rate
	static double crossoverRate = 0.5;
	// mutation rate
	static double mutationRate = 0.08;

	// generate a random chromosome/Traveller starting in the ciny number begin,
	// to the city number end
	private static Traveller generateRandomChromosome(int begin, int end) {
		List<Integer> cityRemaining = new ArrayList<Integer>();
		List<Integer> cityAdded = new ArrayList<Integer>();
		int rand;

		// create a list of position of cities
		for (int k = 0; k < cities.size(); k++) {
			cityRemaining.add(k);
		}

		// remove the list the beginning and the end of the travel
		if (begin < end) {
			cityRemaining.remove(end);
			cityRemaining.remove(begin);
		} else {
			cityRemaining.remove(begin);
			cityRemaining.remove(end);
		}

		// generate a random path for the traveller
		while (!cityRemaining.isEmpty()) {
			rand = (int) (Math.random() * cityRemaining.size());
			cityAdded.add(cityRemaining.get(rand));
			cityRemaining.remove(rand);
		}
		Traveller res = new Traveller(begin, end, cityAdded);
		return res;
	}

	// generate a set of nbChrom random travellers starting in the ciny number
	// begin, to the city number end
	private static Traveller[] generateSet(Integer begin, Integer end) {
		Traveller[] chromosomes = new Traveller[nbChrom];

		// repeat nbChrom times the generation of a chromosome
		for (int k = 0; k < nbChrom; k++) {
			chromosomes[k] = generateRandomChromosome(begin, end);
		}
		return chromosomes;
	}

	// generate a list containing the travel cost of each the chromosomes
	private static double[] calculateTravelCostList(Traveller[] chromosomes) {

		double[] fVals = new double[nbChrom];
		// we determine for each chromosom the value of the function we are
		// trying to maximize
		for (int k = 0; k < nbChrom; k++) {
			// SELECTION FUNCTION : we take the function to maximize + 81
			// (opposite of the minoration of the value of the function (-81),
			// to get positives values)
			fVals[k] = chromosomes[k].totalCostTravel(cities);
		}
		return fVals;
	}

	private static int[] findTwoBestChromosomes(double[] scores) {
		double best = Double.MAX_VALUE;
		double secondBest = Double.MAX_VALUE;
		int index1 = 0;
		int index2 = 1;
		for (int i = 0; i < nbChrom; i++) {
			if (scores[i] < best) {
				secondBest = best;
				best = scores[i];
				index2 = index1;
				index1 = i;
			} else if (scores[i] < secondBest) {
				index2 = i;
				secondBest = scores[i];
			}
		}
		return new int[] { index1, index2 };
	}

	// Select by roulette method
	private static Traveller[] rouletteSelection(Traveller[] chromosomes) {
		double[] scores = calculateTravelCostList(chromosomes);
		Traveller[] nextChromosomes = new Traveller[nbChrom];

		/*
		 * Elitism: Find two best chromosomes Add them to population after
		 * selection is finished making sure best chromosomes never disappear
		 */
		int[] eliteIndex = findTwoBestChromosomes(scores);
		Traveller elite1 = chromosomes[eliteIndex[0]].copyTraveller();
		Traveller elite2 = chromosomes[eliteIndex[1]].copyTraveller();

		// Invert scores and normalize
		double sum = 0;
		for (int i = 0; i < nbChrom; i++) {
			scores[i] = 1 / scores[i];
			sum += scores[i];
		}
		for (int i = 0; i < nbChrom; i++) {
			scores[i] = scores[i] / sum;
		}

		for (int i = 1; i < nbChrom / 2; i++) {
			double rand1 = Math.random();
			double rand2 = Math.random();
			int firstParent = -1;
			int secondParent = -1;
			double cumulation = 0;
			for (int j = 0; j < nbChrom; j++) {
				cumulation += scores[j];
				if (cumulation > rand1 && firstParent == -1)
					firstParent = j;
				if (cumulation > rand2 && secondParent == -1)
					secondParent = j;
			}
			// Add some extra bias towards elites
			if (Math.random() < 0.1)
				firstParent = 0;
			if (Math.random() < 0.1)
				secondParent = 1;

			// Redo iteration if parents are same
			if (chromosomes[firstParent] == chromosomes[secondParent]) {
				i--;
				continue;
			}
			nextChromosomes[2 * i] = chromosomes[firstParent];
			nextChromosomes[2 * i + 1] = chromosomes[secondParent];
		}

		// Add the two elites back into population
		nextChromosomes[0] = elite1;
		nextChromosomes[1] = elite2;
		return nextChromosomes;
	}

	// find the value of a gene out of the two crossover point
	private static int findValueGeneOutCrossover(Traveller[] chromosomes, int chr, int h, List<Integer> newChrom) {
		Integer resTmp = chromosomes[chr].orderVisit.get(h);
		int nextPos;
		// if not present in the crossover point, copy it from the old chromosom
		if (!newChrom.contains(resTmp)) {
			return resTmp;
			// else, replace it by the value of the old chromosom at the
			// replaced gene
		} else {
			nextPos = newChrom.indexOf(resTmp);
			resTmp = chromosomes[chr].orderVisit.get(nextPos);

			while (newChrom.contains(resTmp)) {
				nextPos = newChrom.indexOf(resTmp);
				resTmp = chromosomes[chr].orderVisit.get(nextPos);
			}
			return resTmp;

		}
	}

	// apply the crossover
	private static Traveller[] CrossoverPartiallyMapped(Traveller[] chromosomes) {
		int rand1;
		int rand2;
		int tmp;
		int newVal;

		/*
		 * Part of elitism During the selection we added the two best
		 * chromosomes in beginning of population array. Similarly here, re-add
		 * them after crossover to make sure they don't disappear
		 */
		Traveller elite1 = chromosomes[0].copyTraveller();
		Traveller elite2 = chromosomes[1].copyTraveller();

		// We go through the chromosom list two by two
		for (int k = 1; k < nbChrom / 2; k++) {
			List<Integer> newChrom1 = new ArrayList<Integer>();
			List<Integer> newChrom2 = new ArrayList<Integer>();

			// if a crossover occurs,
			if (Math.random() < crossoverRate) {
				// we generate 2 random crossover points
				rand1 = (int) (Math.random() * chromosomes[2 * k].orderVisit.size());
				rand2 = (int) (Math.random() * chromosomes[2 * k + 1].orderVisit.size());

				// we sort these points
				if (rand2 < rand1) {
					tmp = rand1;
					rand1 = rand2;
					rand2 = tmp;
				}
				// we initialise to null all the genes before first crosover
				// point
				for (int h = 0; h < rand1; h++) {
					newChrom1.add(null);
					newChrom2.add(null);
				}

				// We swap the value of the chromosoms between the two crossover
				// points
				for (int h = rand1; h < rand2 + 1; h++) {
					newChrom1.add(h, chromosomes[2 * k + 1].orderVisit.get(h));
					newChrom2.add(h, chromosomes[2 * k].orderVisit.get(h));
				}
				// before the crossover point, we remove te initialised values
				// and replace them with adequate values
				for (int h = 0; h < rand1; h++) {
					newVal = findValueGeneOutCrossover(chromosomes, 2 * k, h, newChrom1);
					newChrom1.remove(h);
					newChrom1.add(h, newVal);
					newVal = findValueGeneOutCrossover(chromosomes, 2 * k + 1, h, newChrom2);
					newChrom2.remove(h);
					newChrom2.add(h, newVal);
				}
				// after the crossover point, we add the adequate values
				for (int h = rand2 + 1; h < chromosomes[k].orderVisit.size(); h++) {
					newChrom1.add(h, findValueGeneOutCrossover(chromosomes, 2 * k, h, newChrom1));
					newChrom2.add(h, findValueGeneOutCrossover(chromosomes, 2 * k + 1, h, newChrom2));
				}

				chromosomes[2 * k].orderVisit = newChrom1;
				chromosomes[2 * k + 1].orderVisit = newChrom2;
			}
		}
		// Elitism
		chromosomes[0].orderVisit = elite1.orderVisit;
		chromosomes[1].orderVisit = elite2.orderVisit;
		return chromosomes;
	}

	// application of the potentials mutations
	private static Traveller[] mutationTwoElements(Traveller[] chromosomes) {
		int rand1;
		int rand2;
		int tmp;
		// we run through each gene of each chromosome of the set of chromosoms
		// Ignore first element (elite)
		for (int k = 1; k < nbChrom; k++) {
			// if a mutations occurs(randomly determined),
			if (Math.random() < mutationRate) {
				rand1 = (int) (Math.random() * chromosomes[k].orderVisit.size());
				do {
					rand2 = (int) (Math.random() * chromosomes[k].orderVisit.size());
				} while (rand2 == rand1);
				// Then we change the value of two random genes
				tmp = chromosomes[k].orderVisit.get(rand1);
				chromosomes[k].orderVisit.set(rand1, chromosomes[k].orderVisit.get(rand2));
				chromosomes[k].orderVisit.set(rand2, tmp);
			}
		}
		return chromosomes;
	}

	public static void main(String[] args) {

		// Origin cities, and their optimal solutions from brute force solver
		ArrayList<Integer> startPositions = new ArrayList<>(Arrays.asList(0, 1, 2, 8));
		ArrayList<Integer> optimalSolutions = new ArrayList<>(Arrays.asList(42074, 41788, 43238, 44613));
		ArrayList<ArrayList<Double>> results = new ArrayList<>();
		for (int i = 0; i < startPositions.size(); i++) {

			// Array keeping the history of best results up until every
			// generation
			ArrayList<Double> evolution = new ArrayList<>();
			System.out.println("Finding optimal route with origin " + cities.get(startPositions.get(i)).name);
			Traveller[] chromosomes = generateSet(startPositions.get(i), 3);
			Traveller[][] data = new Traveller[nbGener + 1][nbChrom];

			// creation of nbGener new generations
			for (int k = 0; k < nbGener; k++) {
				data[k] = chromosomes.clone();
				chromosomes = rouletteSelection(chromosomes);
				chromosomes = CrossoverPartiallyMapped(chromosomes);
				chromosomes = mutationTwoElements(chromosomes);
			}
			data[nbGener] = chromosomes.clone();

			double bestVal = data[0][0].totalCostTravel(cities);
			Traveller bestChrom = data[nbGener][nbChrom - 1].copyTraveller();
			for (Traveller[] gener : data) {
				for (Traveller chrom : gener) {
					if (chrom.totalCostTravel(cities) < bestVal) {
						bestVal = chrom.totalCostTravel(cities);
						bestChrom = chrom.copyTraveller();
					}
				}
				double percentageScore = 100 - 100 * (bestVal - optimalSolutions.get(i)) / optimalSolutions.get(i);
				if (percentageScore > 100) {
					percentageScore = 100;
				}
				evolution.add(percentageScore);
			}

			results.add(evolution);
			System.out.println(bestChrom.toOneLineString(cities));

		}

		// Write results to file
		// Used for plotting
		try {
			PrintWriter pw = new PrintWriter("evolutions.out", "UTF-8");
			for (int i = 0; i < results.size(); i++) {
				String line = cities.get(startPositions.get(i)).name;
				for (Double value : results.get(i)) {
					line += "," + value;
				}
				pw.println(line);
			}
			pw.close();
		} catch (Exception e) {
			System.err.println("Something went wrong " + e);
		}

	}
}
