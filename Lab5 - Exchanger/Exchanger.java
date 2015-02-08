import java.util.concurrent.Semaphore;
import java.util.concurrent.atomic.AtomicInterger;

class Exchanger{
	static AtomicInteger exchanges = new AtomicInteger(0);
	static Semaphore S;
	
	public Object exchange(Object y){
		
	}
	
	public int getNumExchanges(){
		return exchanges;
	}
}