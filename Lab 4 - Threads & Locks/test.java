import java.io.*;
import java.util.*;
import java.util.concurrent.locks.*;

public class test{
	static int x = 0;
	static Lock L = new ReentrantLock();
	
	public static void main(String[] args){
		Thread[] T = new Thread[2];
		for(int j=0;j<2;++j){
			T[j] = new Thread( () ->
				{
					for(int i = 0; i<100000; i++){
						L.lock();
						try{
							x = x+1;
						} finally{
							L.unlock();
						}
					}
				}
			);
		}
		T[0].start();
		T[1].start();
		try{
			T[0].join();
			T[1].join();
			System.out.println(x);   //Should output 200000
		} catch(InterruptedException e){
			return;
		}
	}
}