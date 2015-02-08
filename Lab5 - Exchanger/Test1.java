public class Test1 {
    public static void main(String[] args) throws Exception{
        Exchanger ex = new Exchanger();
        Thread t1 = new Thread( () -> { 
            int v2 = (Integer) ex.exchange(new Integer(10));
			System.out.println("Thread1: Entered[10], Gets["+v2+"]");
            Assert.Assert(v2==20);
        });
        Thread t2 = new Thread( () -> { 
            int v2 = (Integer) ex.exchange(new Integer(20));
			System.out.println("Thread2: Entered[20], Gets["+v2+"]");
            Assert.Assert(v2==10);
        });
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println("OK");
    }
    
}
