public class Test1 {
    public static void main(String[] args) throws Exception{
        Exchanger ex = new Exchanger();
        Thread t1 = new Thread( () -> { 
            try{
                int v2 = (Integer) ex.exchange(new Integer(10));
                Assert.Assert(v2==20);
            }
            catch(InterruptedException e){
                System.exit(1);
            }
        });
        Thread t2 = new Thread( () -> { 
            try{
                int v2 = (Integer) ex.exchange(new Integer(20));
                Assert.Assert(v2==10);
            }
            catch(InterruptedException e){
                System.exit(1);
            }
        });
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println("OK");
    }
    
}
