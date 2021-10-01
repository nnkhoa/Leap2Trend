import java.io.*;
import java.util.*;

public class FindingPosition {

	public static void main(String[] args) {
		try {
			String path = "";
			String fileName = "Positions.txt";
			String keyWordList = "kw_list.txt";
			String filePW = "RankedKeywords.txt";
			String line = "";
			int i = 0;

			Scanner inFile1 = new Scanner(new File(keyWordList));

			// Original answer used LinkedList, but probably preferable to use ArrayList in most cases
			// List<String> temps = new LinkedList<String>();
			List<String> temps = new ArrayList<String>();
			String token1 = "";
			// while loop
			while (inFile1.hasNext()) {
			// find next line
				token1 = inFile1.next();
				temps.add(token1);
			}
			inFile1.close();

    		String[] keyWords = temps.toArray(new String[0]);
			// String[] keyWords = { "gaussian_process", "reinforcement_learning", "neural_networks", "semi_supervised",
			// 		"active_learning", "graphical_models", "machine_learning", "decision_making", "bayesian_inference",
			// 		"nearest_neighbor", "feature_selection", "time_series", "gradient_descent", "spectral_clustering",
			// 		"monte_carlo", "spiking_neurons", "belief_propagation", "multi_agent", "supervised_learning",
			// 		"hidden_markov" };
			PrintWriter pw = new PrintWriter(path + filePW);
			BufferedReader bf = new BufferedReader(new FileReader(path + fileName));
			while ((line = bf.readLine()) != null) {
				i++;
				String pos1 = line.substring(line.indexOf("is") + 3, line.indexOf(","));
				String pos2 = line.substring(line.indexOf(",") + 1, line.length());
				int p1 = Integer.parseInt(pos1);
				int p2 = Integer.parseInt(pos2);
				System.out.println(keyWords[p1] + "---" + keyWords[p2]);
				pw.write(i + ") " + keyWords[p1] + "---" + keyWords[p2]);
				pw.println();

			}
			bf.close();
			pw.close();

		} catch (IOException e) {
			System.out.println(e.getMessage());

		}
	}
}
