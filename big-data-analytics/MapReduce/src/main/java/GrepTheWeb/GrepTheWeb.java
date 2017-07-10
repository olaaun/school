package GrepTheWeb;

public class GrepTheWeb {

	public static void main(String[] args) throws Exception {
		if (args.length != 3) {
			System.out.println("Grep <inDir> <outDir> <regex>");
			System.exit(2);
		}
		String input = args[0];
		String output = args[1];
		String regex = args[2];
		ProcessBuilder pb = new ProcessBuilder("python", "GrepTheWeb" + ".py",
				input, output, regex).inheritIO();
		Process p = pb.start();
		p.waitFor();
		System.exit(0);

	}

}