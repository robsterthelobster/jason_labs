import java.util.*;
import java.util.concurrent.atomic.*;

class Test3{
    class Ob implements Runnable{
        int x;
        int y;
        Ob(int x){
            this.x=x;
        }
        public void run(){
            Random r = new Random();
            
            int y=this.x;
            
            try{
				while( Test3.keepgoing.get() ){
					Thread.sleep(r.nextInt(100));
					y = (Integer) Test3.ex.exchange(new Integer(y));
				}
				this.y = y;
            }
            catch(InterruptedException e){
                System.exit(1);
            }
        }
    }

    class Helper implements Runnable{
        int x;
        Helper(int x){
            this.x=x;
        }
        public void run(){
            //try{
            Test3.ex.exchange(new Integer(x));
            //} catch(InterruptedException e){
            //    System.exit(0);
            //}
        }
    }

    static Exchanger ex = new Exchanger();
    static AtomicBoolean keepgoing = new AtomicBoolean(true);
    
    public static void main(String[] args) throws Exception{
        new Test3();
    }
    
    Test3() throws Exception{
        
        ArrayList<Thread> T = new ArrayList<>();
        ArrayList<Ob> O = new ArrayList<>();
        
        TreeSet<Integer> expected = new TreeSet<>();
        
        for(int i=0;i<20;++i){
            Ob o = new Ob(i*10);
            expected.add(i*10);
            Thread t= new Thread(o,"W-"+i);
            T.add(t);
            O.add(o);
        }
        for(Thread t : T )
            t.start();
            
        System.out.println("Workin'...");
        Thread.sleep(5000);
        keepgoing.set(false);
        System.out.println("Worked.");
        
        TreeSet<Integer> actual = new TreeSet<>();
        while(T.size() > 0 ){
            T.get(0).join(2000);
            if( !T.get(0).isAlive() ){
                T.remove(0);
            }
            else{
                Helper h = new Helper(-1);
                expected.add(-1);
                actual.add(-1);
                Thread t = new Thread(h);
                t.start();
                t.join();
            }
        }

        for(Ob o : O ){
            actual.add(o.y);
        }
        
        //uncomment to see content of arrays
        System.out.println(expected);
        System.out.println(actual);
        
        Assert.Assert(expected.equals(actual));
        
        System.out.println("OK: Performed "+ex.getNumExchanges()+" exchanges");
    }
}
