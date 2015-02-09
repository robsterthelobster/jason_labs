
import java.util.*;
import java.util.regex.*;

public class JSONParser{
    
    int pos;
    String input;
    Object parse(String input){
        this.input=input;
        TreeMap<String,Object> M = new TreeMap<>();
        pos=0;
        
        whitespace();
        if( input.charAt(pos) == '{' )
            return dictionary();
        else if( input.charAt(pos) == '[' )
            return list();
        else
            throw new RuntimeException("Unexpected character:"+input.charAt(pos));
        
    }
    
    Map<String,Object> dictionary(){
        TreeMap<String,Object> M = new TreeMap<>();
        
        consume("{");
        
        while(true){
            
            whitespace();
            String key = string();
            whitespace();
            consume(":");
            whitespace();
            Object val = thing();
            
            
            M.put(key,val);
            whitespace();
            if(peek(",")){
                consume(",");
            }
            else if( peek("}") ){
                consume("}");
                return M;
            }
            else{
                error();
            }
        }
    }
    
    Object thing(){
        if( peek("null") ){
            consume("null");
            return null;
        }
        else if( peek("[") ){
            return list();
        }
        else if( peek("{") ){
            return dictionary();
        }
        else if( peek("\"") ){
            return string();
        }
        else if( (input.charAt(pos) >= '0' && input.charAt(pos) <= '9') || input.charAt(pos) == '-' ){
            return number();
        }
        else if( peek("true") ){
            pos += 4;
            return new Boolean(true);
        }
        else if( peek("false") ){
            pos += 5;
            return new Boolean(false);
        }
        else{
            error();
            return null; //never happens
        }
    }
    List<Object> list(){
        List<Object> L = new ArrayList<>();
        consume("[");
        while(true){
            whitespace();
            L.add(thing());
            whitespace();
            if( peek(",") )
                consume(",");
            else if( peek("]") ){
                consume("]");
                return L;
            }
            else
                error();
        }
    }
    
    Double number(){
        Pattern p = Pattern.compile("[-\\dEe+.]+");
        Matcher m = p.matcher(input);
        if( m.find(pos) ){
            if( m.start(0) == pos ){
                String tmp = input.substring(pos,pos+m.group(0).length());
                double d = Double.parseDouble(tmp);
                pos += m.group(0).length();
                return new Double(d);
            }
            else{
                error("Not number");
            }
        }
        else{
            error("Not a number");
        }
        return null;
        
    }
    
    void error(){
        error("?");
    }
    
    void error(String msg){
        throw new RuntimeException(msg+": --->"+input.substring(pos,pos+30)+"<---");
    }
    
    boolean peek(String s){
        for(int i=0;i<s.length();++i){
            if( i+pos < input.length() && input.charAt(i+pos) == s.charAt(i) )
                ;
            else
                return false;
        }
        return true;
    }
    
    void whitespace(){
        while( input.charAt(pos) == ' ')
            pos++;
    }
   
    void consume(String s){
        if( !peek(s) )
            error();
        pos += s.length();
    }
    
    String string(){
        consume("\"");
        String s="";
        while( input.charAt(pos) != '"' )
            s += input.charAt(pos++);
        consume("\"");
        return s;
    }
        
    //for testing
    static void dump(Object o){
        if( o == null ){
            System.out.print("null");
        }
        else if( o instanceof String ){
            System.out.print( "\"" + (String) o + "\"" );
        }
        else if( o instanceof Map ){
            System.out.print("{");
            Map<String,Object> m = (Map<String,Object>) o;
            boolean flag=false;
            for( String k : m.keySet() ){
                if(flag )
                    System.out.print(",");
                flag=true;
                System.out.print(k+":");
                dump(m.get(k));
            }
            System.out.print("}");
        }
        else if( o instanceof List ){
            List<Object> L = (List<Object>) o;
            System.out.print("[");
            boolean flag=false;
            for( Object x : L ){
                if(flag)
                    System.out.print(",");
                flag=true;
                dump(x);
            }
            System.out.print("]");
        }
        else if( o instanceof Double ){
            System.out.print(((Double) o ) );
        }
        else if( o instanceof Boolean ){
            System.out.print( (Boolean) o );
        }
        else{
            System.out.print("?");
        }
    }
    
        
    //test suite
    public static void main(String[] args){
        JSONParser p = new JSONParser();
        Object r = p.parse(args[0]);
        dump(r);
        
    }
}
