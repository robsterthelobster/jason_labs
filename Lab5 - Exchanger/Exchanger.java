import java.util.concurrent.Semaphore;
import java.util.ArrayList;

class Exchanger{
	static Semaphore S1 = new Semaphore(0);
	static Semaphore S2 = new Semaphore(1);
	static int n = 2;
	static int exchanges = 0;
	static ArrayList obj = new ArrayList();
	
	public Object exchange(Object y){
		Object tmp = null;
		try{
			obj.add(y);
			n -= 1;
			if(n == 0){
				S1.release();
				S1.release();
			}
			S1.acquire();
			S2.acquire();
			for(int i = 0; i < obj.size(); i++){
				tmp = obj.get(i);
				if(y != tmp){
					tmp = obj.remove(i);
					S2.release();
					break;
				}
			}
		} catch(InterruptedException e){
			System.out.println(e);
		}
		return tmp;
	}
	
	public int getNumExchanges(){
		return exchanges;
	}
}