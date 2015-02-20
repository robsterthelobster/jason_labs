import java.util.concurrent.*;
import java.util.concurrent.locks.*;
import java.util.ArrayList;

class Exchanger{
	static Lock L = new ReentrantLock();
	static Semaphore s1 = new Semaphore(0);
	static Semaphore s2 = new Semaphore(1);
	static Semaphore s3 = new Semaphore(2);
	static ArrayList objs = new ArrayList();
	static Object tmp = null;
	static int exchanges = 0;
	static int numThreads = 0;
	static boolean displayPrints = false;
	
	public Object exchange(Object y){
		try{
			s3.acquire();
			numThreads++;
			int threads = numThreads;
			if(displayPrints)
				System.out.println("Thread["+threads+"]: s3 acquired, left: " + s3.availablePermits());
			s2.acquire();
			if(displayPrints)
				System.out.println("Thread["+threads+"]: s2 acquired");
			if(objs.isEmpty()){
				try{
					objs.add(y);
					s2.release();
					if(displayPrints){
						System.out.println("Thread["+threads+"]: s2 release, current: " + s2.availablePermits());
						System.out.println("Thread["+threads+"]: Stop");
					}
					s1.acquire();
					if(displayPrints)
						System.out.println("Thread["+threads+"]: Go");
					return objs.remove(0);
				} finally{
					if(displayPrints)
						System.out.println("Thread["+threads+"]: Done");
					s2.release();
					s3.release();
					s3.release();
					exchanges++;
					if(displayPrints){
						System.out.println("s3: " + s3.availablePermits());
						System.out.println("s2: " + s2.availablePermits());
						System.out.println("s1: " + s1.availablePermits());
					}
				}
			} else{
				if(displayPrints)
					System.out.println("Thread["+threads+"]: Go");
				objs.add(y);
				try{
					return objs.remove(0);
				} finally{
					s1.release();
					if(displayPrints)
						System.out.println("Thread["+threads+"]: Done");
				}
			}
		} catch(InterruptedException e){
			System.out.println(e);
			return null;
		}
	}
	
	public int getNumExchanges(){
		return exchanges;
	}
}