import java.io.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.*;

public class Count{
    //static int count=0;
	static AtomicInteger count = new AtomicInteger(0);
    
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
            raf = new RandomAccessFile(fname,"r");
            Thread[] T = new Thread[numthreads];
            for(int i=0;i<numthreads;++i){
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
            long filesize = raf.length();
            long sz = filesize / totaltasks;
            long start = myid*sz;
			System.out.println("myid["+this.myid+"] tasks["+this.totaltasks+"] size["+filesize+"] sz["+sz+"] start["+start+"]");
			raf.seek(start);
			if(start != 0 )
				raf.readLine();
			while(raf.getFilePointer() < filesize ){
				String s = raf.readLine();
				Scanner sc = new Scanner(s);
				while(sc.hasNext()){
					String w = sc.next();
					System.out.println("["+this.myid+"]: "+w);
					if( w.startsWith("http://")){
						Count.count.incrementAndGet();
					}
				}
			}
		} catch(IOException e){
            System.out.println("IO error!");
        }
    }
}