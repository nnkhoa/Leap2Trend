import java.io.*;

public class RankExtraction {

	public static void main(String[] args) {
		String pathFolder = "/Users/khoanguyen/Workspace/git/Leap2Trend/top20kw/";
		String pathPW = "Ranking1.txt";
		String file1 = "kw_list.txt";
		String line, fileName, lineFileName, rank;
		File folder = new File(pathFolder);

		try {
			BufferedReader bfFile1 = new BufferedReader(new FileReader(file1));
			BufferedReader bfFileName = null;
			PrintWriter pw = new PrintWriter(pathPW);
			while ((line = bfFile1.readLine()) != null) {
				String keyword = line.substring(line.indexOf(")") + 1, line.length());
				pw.println(keyword);
				System.out.println(keyword);
				if (folder.isDirectory()) {
					for (File f : folder.listFiles()) {
						fileName = f.getName();
						if (!folder.getName().equals(".DS_Store")) {
							bfFileName = new BufferedReader(new FileReader(pathFolder + fileName));
							while ((lineFileName = bfFileName.readLine()) != null) {
								if (lineFileName.contains(keyword)) {
									rank = lineFileName.substring(0, lineFileName.indexOf(')'));
									System.out.println("The Rank of the keywords " + keyword + " in the file " + fileName
											+ " is " + rank);
									pw.println();
									pw.print("The Rank of the keywords in the file " + fileName + " is " + rank);
									pw.println();
									break;
								}

							}
							bfFileName.close();
						}

					}
					pw.println("*******");
				}
			}
			bfFile1.close();
			pw.close();

		} catch (IOException e) {
			System.out.println(e.getMessage());
		}
		System.out.println("******** Done!!!!! ********");
	}
}
