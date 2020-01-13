package Maventest;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.io.PrintWriter;
import java.io.Writer;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.jsoup.HttpStatusException;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ser.std.StdSerializer;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.module.SimpleModule;




/**
 * Hello world!
 *
 */

public class Gather

{
    public static String urlbase = "http://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/";
    public static String urlpage = "giin.htm";
    //ArrayListを宣言

    public static class Pol {
        String name;
        String party;
        String house;
        String consecutive;
        String district;
        //ArrayList<String> education;
        //ArrayList<String> family;
        //ArrayList<String> previously; 
        List<String> education = new ArrayList<String> ();
        List<String> family = new ArrayList<String> (); 
        List<String> previously = new ArrayList<String>(); 
        String website;
        String wikiurl;
       }
    
    public static class Results {
        //ArrayList<String> education;
        //ArrayList<String> family;
        //ArrayList<String> previously; 
        public List<String> education = new ArrayList<String> ();
        public List<String> family = new ArrayList<String> (); 
        public List<String> previously = new ArrayList<String>();  
        public String website = "empty";
        public String wikiurl = "empty";
    } 
    
    public static Results wikisearch (String rep) throws IOException {
        Results a = new Results();

        try {
        String url = "https://ja.wikipedia.org/w/index.php?sort=relevance&search="+rep+"+%28政治家%29+deepcat%3A存命人物+hastemplate%3A政治家&title=%E7%89%B9%E5%88%A5:%E6%A4%9C%E7%B4%A2&profile=advanced&fulltext=1&advancedSearch-current=%7B%22fields%22%3A%7B%22plain%22%3A%5B%22%E6%94%BF%E6%B2%BB%22%5D%7D%7D&ns0=1";
        String connectto = Jsoup.connect(url).get().select(".searchresults ul li div a").attr("href").toString();
        Document document = Jsoup.connect("https://ja.wikipedia.org"+connectto).get();
        Elements selected = document.select(".infobox");
        

        ///////////////////////////// education ///////////////////////////////////////
        
        if (selected.select("th:contains(出身校)").next().text().equals("")){
            System.out.println(rep+ "not found in text   " + selected);
        } else {
            System.out.println(rep+ "found!!!!!!!!!!!!!!!   " + selected.select("th:contains(出身校)"));
            for (String b : selected.select("th:contains(出身校)").next().select("td").eachText()) {
                String[] splited = b.split("\\s+");
                for (String c : splited) {
                    a.education.add(c);
                }
            }
        }
        if (selected.select("th:contains(親族)").next().text().equals("")){
            System.out.println(rep+ "not found in text   " + selected);
        } else {
            System.out.println(rep+ "found!!!!!!!!!!!!!!!   " + selected.select("th:contains(親族)"));
            for (String b : selected.select("th:contains(親族)").next().select("td").eachText()) {
                String[] splited = b.split("\\s+");
                for (String c : splited) {
                    a.family.add(c);
                }
            }
        }
        if (selected.select("th:contains(前職)").next().text().equals("")){
            System.out.println(rep+ "not found in text   " + selected);
        } else {
            System.out.println(rep+ "found!!!!!!!!!!!!!!!   " + selected.select("th:contains(前職)"));
            for (String b : selected.select("th:contains(前職)").next().select("td").eachText()) {
                String[] splited = b.split("\\s+");
                for (String c : splited) {
                    a.previously.add(c);
                }
            }
        }
        
        a.wikiurl = "https://ja.wikipedia.org"+connectto;
        return a;

        } catch (HttpStatusException e) {
            System.out.println(rep+ "  education data unavailable");
            return a;
        }
    }


    public static class WriterCustomSerializer extends StdSerializer<Pol> {
        
        public WriterCustomSerializer() {
            this(null);
        }
       
        public WriterCustomSerializer(Class<Pol> t) {
            super(t);
        }

        @Override
        public void serialize(
          Pol value, JsonGenerator jgen, SerializerProvider provider) 
          throws IOException, JsonProcessingException {
      
            jgen.writeStartObject();
            jgen.writeStringField("name", value.name);
            jgen.writeStringField("party", value.party);
            jgen.writeStringField("house", value.house);  
            jgen.writeStringField("district", value.district);
            jgen.writeStringField("consequtive", value.consecutive);        
            jgen.writeFieldName("education");
            jgen.writeStartArray();
            for (String eduelement : value.education) {
                jgen.writeString(eduelement);
            }
            jgen.writeEndArray();
            jgen.writeFieldName("family");
            jgen.writeStartArray();
            for (String famelement : value.family) {
                jgen.writeString(famelement);
            }
            jgen.writeEndArray();
            jgen.writeFieldName("previously");
            jgen.writeStartArray();
            for (String preelement : value.previously) {
                jgen.writeString(preelement);
                
            }
            jgen.writeEndArray();
            jgen.writeStringField("website", value.website);
            jgen.writeStringField("wikiurl", value.wikiurl);    
            jgen.writeEndObject();    
        }
        @Override
        public Class<Pol> handledType() {
        return Pol.class;
        }

        
    }
    public static void main(String[] args) throws IOException {
        List<Pol>reps = new ArrayList<Pol>();
        for (int urlnum = 1; urlnum<11; urlnum++) {
        
        String connectto = urlbase+urlnum+urlpage;
        System.out.println(connectto);

        Document document = Jsoup.connect(connectto).get();
        Elements selected = document.select("tr[valign=top]");
        
        for (Element onerep : selected) {
            Pol politician = new Pol();
            String name = onerep.select(".sh1td5 .sh1tt1 a").text().replace("君", "");
            String party = onerep.select(".sh1td7 .sh1tt1 center").text();
            String consecutive = onerep.select(".sh1td8 .sh1tt1 center").text().replace("　", "").replace(" ", "");
            String district = onerep.select(".sh1td5 .sh1tt1").text().replace(name, "").replace("君", "").replace("　", "").replace(" ", "");
            if (name.equals("")){
                continue;
            }
            politician.name = name; 
            politician.party = party;
            politician.consecutive = consecutive;
            politician.district = district;

            Results a = wikisearch(name.replace("　", "").replace(" ", ""));
            politician.education = a.education;
            politician.family = a.family;
            politician.previously = a.previously;
            politician.website = a.website;
            politician.wikiurl = a.wikiurl;
            
            reps.add(politician);
            System.out.println(politician.name);
            System.out.println(politician.party);
            System.out.println("politician.education >>> "+politician.education);
            System.out.println(politician.family);
            System.out.println(politician.previously);
            System.out.println(politician.website);
            System.out.println(politician.wikiurl);
            System.out.println("====================================================");
            
            /*
            if (onerep == selected.get(1)){
            break;
        }
        */
            }
        } 
    
    Integer educationi = 0;
    Integer familyi = 0;
    Integer previ = 0;
    Integer websi = 0;
    for (Pol rep : reps) {
        if (rep.education == null){
            educationi++;
        }  
        if (rep.family == null){
            familyi++;
        }
        if (rep.previously == null){
            previ++;
        }
        if (rep.website.equals("empty")){
            websi++;
        }
    }
    System.out.println("education >>>> "+educationi);
    System.out.println("family >>>> "+familyi);
    System.out.println("previously >>>> "+previ);
    System.out.println("websi >>>> "+websi);
    System.out.println(reps.size());

    Pol stats = new Pol();

    stats.name = "stats";
    System.out.println(stats.name);
    stats.education.add(educationi.toString());
    stats.family.add(familyi.toString());
    stats.previously.add(previ.toString());
    stats.website = websi.toString();
    
    reps.add(stats);

    ObjectMapper mapper = new ObjectMapper();
    
    SimpleModule module = new SimpleModule();
    module.addSerializer(new WriterCustomSerializer());
    mapper.registerModule(module);

    Writer out = new PrintWriter("java/giin/test/test.json");
    mapper.writerWithDefaultPrettyPrinter().writeValue(out, reps);
    out.close();
    
    }
}


