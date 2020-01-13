package Maventest;

import java.io.IOException;
import java.util.ArrayList;
import java.io.PrintWriter;
import java.io.Writer;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Properties;
import java.nio.charset.StandardCharsets;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.Response;



class Config {
    public static String gkey; 
    public static String gid;
}


public class Analyze
{
	public static void main(String[] args) throws IOException {
        Properties properties = new Properties();
        try {
            properties.load(Files.newBufferedReader(Paths.get("java/test/src/main/java/Maventest/config.properties"), StandardCharsets.UTF_8));
            Config.gkey = properties.getProperty("gkey");
            System.out.println(Config.gkey);
            Config.gid = properties.getProperty("gid");
            System.out.println(Config.gid);
        } catch (IOException e) {
            // ファイル読み込みに失敗
            System.out.println("ファイルの読み込みに失敗しました。ファイル名");
        }
        
        String base = "https://www.googleapis.com/customsearch/v1?key="+Config.gkey+"&cx="+Config.gid+"&q="; 
        
        ObjectMapper mapper = new ObjectMapper();
        JsonNode root = mapper.readTree(new File("test.json"));

        for (JsonNode rep : root) {
            OkHttpClient client = new OkHttpClient();
            String url = base+rep.get("name").toString().replace("\"", "")+"  (公式 or オフィシャル) 議員 -wikipedia　-twitter (サイト or ホームページ)";
            Request request = new Request.Builder().url(url).build();
            Response response = client.newCall(request).execute();
            JsonNode body = mapper.readTree(response.body().string());
            System.out.println(url);
            
            try {
                System.out.println(body.get("items").get(0).get("link"));
                System.out.println(body.get("items").get(0).get("title"));
            } catch (Exception e) {
                System.out.println(body.toPrettyString());
            }

            if (rep == root.get(20)) {
                break;
            } 
            if (body.get("items").get(0).get("link").toString().contains("wikipedia")) {
                System.out.println(body.get("items").get(0).get("link")+"<<<<<<<<<<<<<<<<<");
            }

            //String connectto = "a";
            //Document document = Jsoup.connect(connectto).get();

        }
	}
}
