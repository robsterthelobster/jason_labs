import java.util.*;

public class Test2{
    class Ob implements Runnable{
        int x;
        int y;
        Ob(){
        }
        public void run(){
            //try{
            Random r = new Random();
            this.x = r.nextInt();
            try{
                Thread.sleep(r.nextInt(1000));
            } catch(InterruptedException e){
                System.exit(1);
            }
            
            int y = (Integer) Test2.ex.exchange(new Integer(x));
            this.y=y;
            //}
            //catch(InterruptedException e){
            //    System.exit(1);
            //}
        }
    }

    static Exchanger ex = new Exchanger();
    public static void main(String[] args) throws Exception{
        new Test2();
    }
    
    Test2() throws Exception{
        ArrayList<Thread> T = new ArrayList<>();
        ArrayList<Ob> O = new ArrayList<>();
        
        for(int i=0;i<20;++i){
            Ob o = new Ob();
            Thread t= new Thread(o);
            T.add(t);
            O.add(o);
        }
        for(Thread t : T )
            t.start();
        for(Thread t : T )
            t.join();

        TreeSet<Integer> s1 = new TreeSet<>();
        TreeSet<Integer> s2 = new TreeSet<>();
        for(Ob o : O ){
            s1.add(o.x);
            s2.add(o.y);
        }
        
        
        Assert.Assert(s1.equals(s2));
        
        System.out.println("OK");
    }
    
}
