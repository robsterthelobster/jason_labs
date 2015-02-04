import java.io.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.Semaphore;

public class Count{
	static AtomicInteger count = new AtomicInteger(0);
    static Semaphore L;
    public static void main(String[] arg){
        Scanner in = new Scanner(System.in);
        String fname;
        int numthreads;
        if( arg.length > 0 ){
            fname = arg[0];
            numthreads = Integer.parseInt(arg[1]);
        }
        else{
            System.out.println("File?");
            fname = in.nextLine();
            System.out.println("Num threads?");
            numthreads = in.nextInt();
        }
        
        RandomAccessFile raf;
        try{
			L = new Semaphore(0);
            raf = new RandomAccessFile(fname,"r");
            Thread[] T = new Thread[numthreads];
            for(int i=0;i<numthreads;i++){
                T[i] = new Thread(new Task(i,numthreads,raf));
                T[i].start();
            }
			for(Thread temp : T){
				try{
					temp.join();
				} catch(InterruptedException e){
					return;
				}
			}
            System.out.println("The total is: "+count);
        }
        catch(IOException e){
            System.out.println("Could not read file");
        }
    }
}

class Task implements Runnable{
    int myid;
    int totaltasks;
    RandomAccessFile raf;
	
    public Task(int myid, int totaltasks, RandomAccessFile raf){
        this.myid=myid;
        this.totaltasks=totaltasks;
        this.raf=raf;
    }
    @Override
    public void run(){
        try{
            long filesize = this.raf.length();
            long sz = filesize / this.totaltasks;
            long start = this.myid*sz;
			long end;
			if (this.totaltasks-1 == this.myid)
				end = filesize;
			else
				end = (this.myid+1)*sz;
			System.out.println("myid["+this.myid+"] start["+start +"] end["+end+"]");
			raf.seek(start);
			if(start != 0 )
				raf.readLine();
			while(raf.getFilePointer() < end){
				try{
					Count.L.tryAcquire();
					String s = raf.readLine();
					Scanner sc = new Scanner(s);
					while(sc.hasNext()){
						String w = sc.next();
						System.out.println("["+this.myid+"]: "+ w);
						if( w.startsWith("http://")){
							Count.count.incrementAndGet();
						}
					}
				} finally{
					Count.L.release();
				}
			}
		} catch(IOException e){
            System.out.println("IO error!");
		}
	}
}