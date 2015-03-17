import java.util.*;
import java.lang.System;
import java.io.*;
import javax.imageio.*;
import java.awt.image.BufferedImage;
import java.awt.Color;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.locks.*;

class blur{

	static Scanner scan = new Scanner(System.in);
	static Thread[] threadList;
	static File[] allFiles;
	static int blurLength = 25;
	static BufferedImage img;
	static BufferedImage tmpImg;
	static int currentTotalPixels = 0;
	static CyclicBarrier CB;
	static Lock L = new ReentrantLock();

	public static void main(String[] args){
		String pattern = "";
		int threads = 0;
		int numPasses = 0;
		int blurSize = 25;
		if(args.length == 3){
			pattern = args[0];
			threads = Integer.parseInt(args[1]);
			numPasses = Integer.parseInt(args[2]);
		}else{
			System.out.println("Enter filename pattern: ");
			pattern = scan.nextLine();
			//pattern = "test%d.png";
			System.out.println("Enter number of threads: ");
			threads = scan.nextInt();
			//threads = 4;
			System.out.println("Enter number of passes: ");
			numPasses = scan.nextInt();
			//numPasses = 2;
		}
		long startTime = System.currentTimeMillis();
		
		/*
		System.out.println("Filename pattern : " + pattern);
		System.out.println("Number of threads: " + threads);
		System.out.println("Number of passes : " + numPasses);
		*/
		
		allFiles = getFiles(pattern);
		
		threadList = new Thread[threads];
		
		if(allFiles.length == 0){
			System.out.println("No files with \"" + pattern + "\" pattern found!");
		} else{
			//Currently will start and run threads for each file one at a time
			for(File file : allFiles){
				for(int currPass = 0; currPass < numPasses; currPass++){
					try{
						if(currPass == 0){
							img = ImageIO.read(file);
							tmpImg = new BufferedImage(img.getWidth(),img.getHeight(),img.getType());
							currentTotalPixels = img.getWidth() * img.getHeight();
						} else if(currPass%2 == 1){
							img = tmpImg;
						} else{
							tmpImg = img;
						}
					} catch(IOException e){
						System.out.println(e);
					}
					
					System.out.println(file.getName() + ", Pass: "+ (currPass+1) +" Start!");
					
					//------------THREADS-------------
	
					//Start threads
					for(int i = 0; i < threads; i++){
						threadList[i] = new iThread(i, threads, blurSize);
						threadList[i].start();
					}
					
					//Join threads
					for(int i = 0; i < threads; i++){
						try{
							threadList[i].join();
						} catch(InterruptedException e){
							return;
						}
					}
					
					CyclicBarrier CB = new CyclicBarrier(threads);
					
				}
				//Test
				try{
					File outputfile = new File("BLUR-"+file.getName());
					ImageIO.write(tmpImg, "JPG", outputfile);
				}catch(IOException e){
					System.out.println(e);
				}
				
				System.out.println(file.getName() + " Done!");
			}
			
			long endTime = System.currentTimeMillis();
			long time = endTime - startTime;
			System.out.println("Time: " + time + "ms");
		}
	}
	
	public static class iThread extends Thread{
		int index, blurSize, start, end, imgWidth;
		int rStart, rEnd, cStart, cEnd;
		static int percent = 0;
		static int oldP = 0;
		static int count = 0;
		
		public iThread(int index, int threads, int blurSize){
			this.index = index;
			this.blurSize = blurSize;
			this.imgWidth = img.getWidth();
			this.start = index * img.getHeight()/threads;
			this.end   = (index+1) * img.getHeight()/threads;
			CB = new CyclicBarrier(threads);
		}
		
		public void run(){
			try{
				int halfBlur = (this.blurSize-1)/2;
				for(int y = this.start; y < this.end; y++){
					for(int x = 0; x < this.imgWidth; x++){
						//If box is smaller, cuts off edges
						if(y - halfBlur >= 0)
							rStart = y-halfBlur;
						else
							rStart = 0;
						if(y + halfBlur <= this.end)
							rEnd = y+halfBlur;
						else
							rEnd = this.end;
						if(x - halfBlur >= 0)
							cStart = x-halfBlur;
						else
							cStart = 0;
						if(x + halfBlur <= this.imgWidth)
							cEnd = x+halfBlur;
						else
							cEnd = this.imgWidth;
						
						int blurRGB = getBlurRGB(rStart, rEnd, cStart, cEnd);
						try{
							L.lock();
							//Set RGB value to new image
							tmpImg.setRGB(x, y, blurRGB);
							//Updates image completion
							updatePercent();
						} finally{
							L.unlock();
						}	
					}
				}
				//System.out.println("Thread["+this.index+"] waiting...");
				CB.await();
				//System.out.println("Thread["+this.index+"] go!");
			} catch(InterruptedException e){
				System.out.println(e);
			} catch(BrokenBarrierException e){
				System.out.println(e);
			}
		}
		
		public int getBlurRGB(int rStart, int rEnd, int cStart, int cEnd){
			
			int pixels = (rEnd-rStart)*(cEnd-cStart);
			int tmpR = 0;
			int tmpG = 0;
			int tmpB = 0;
			int RGB = 0;
			//For loops to get 25x25 px area
			for(int r = rStart; r < rEnd; r++){
				for(int c = cStart; c < cEnd; c++){
					//Grab RGB values
					RGB = img.getRGB(c,r);
					tmpR +=((0x00ff0000 & RGB) >> 16);
					tmpG +=((0x0000ff00 & RGB) >> 8);
					tmpB +=((0x000000ff & RGB));
				}
			}
			tmpR = tmpR/pixels;
			tmpG = tmpG/pixels;
			tmpB = tmpB/pixels;
			
			return new Color(tmpR,tmpG,tmpB).getRGB();
		}
		
		public void updatePercent(){	
			count++;
			percent = count*100/currentTotalPixels;
			if(percent > oldP){
				System.out.format("%7d"+"/"+"%7d pixels left... %3d%% done\n",count,currentTotalPixels,percent);
				oldP = percent;
			}
			if(percent == 100){
				count = 0;
				oldP = 0;
			}
		}
	}
	
	public static File[] getFiles(String pattern){
		File dir = new File(".");
		File[] files = dir.listFiles();
		File[] temp = new File[files.length];
		int index = 0;
		while(true){
			String filename = String.format(pattern, index);
			if(!(new File(filename).exists()))
				break;
			else{
				temp[index] = new File(filename);
				index++;
			}
		}
		File[] images = new File[index];
		for(int i = 0; i < images.length; i++)
			images[i] = temp[i];
		return images;
	}
}