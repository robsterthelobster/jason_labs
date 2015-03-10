import java.util.*;
import java.lang.System;
import java.io.*;
import javax.imageio.*;
import java.awt.image.BufferedImage;
import java.awt.Color;
import java.util.concurrent.locks.*;

class blur{

	static Scanner scan = new Scanner(System.in);
	static Thread[] threadList;
	static File[] allFiles;
	static int blurLength = 25;
	static BufferedImage img;
	static BufferedImage tmpImg;
	static Lock L = new ReentrantLock();
	static int currentTotalPixels = 0;

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
			System.out.println("Enter number of threads: ");
			threads = scan.nextInt();
			System.out.println("Enter number of passes: ");
			numPasses = scan.nextInt();
		}
		long startTime = System.currentTimeMillis();
		
		/*
		System.out.println("Filename pattern : " + pattern);
		System.out.println("Number of threads: " + threads);
		System.out.println("Number of passes : " + numPasses);
		*/
		
		allFiles = getFiles(pattern);
		
		if(allFiles.length == 0){
			System.out.println("No files with \"" + pattern + "\" pattern found!");
		}/*else if(allFiles.length > 0){
			for(int x = 0; x < allFiles.length; x++){
				System.out.println("File: " + allFiles[x].getName());
			}
		}
		*/
		
		//Currently will start and run threads for each file one at a time
		for(File file : allFiles){
			try{
				img = ImageIO.read(file);
				tmpImg = new BufferedImage(img.getWidth(),img.getHeight(),img.getType());
				currentTotalPixels = img.getWidth() * img.getHeight();
			} catch(IOException e){
				System.out.println(e);
			}
			
			System.out.println(file.getName() + " Start!");
			
			//------------THREADS-------------
			threadList = new Thread[threads];
			
			//Create threads and start
			for(int i = 0; i < threads; i++){
				threadList[i] = new iThread(i, threads, numPasses, blurSize);
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
			
			//Test
			try{
				File outputfile = new File("BLUR-"+file.getName());
				ImageIO.write(tmpImg, "JPG", outputfile);
			}catch(IOException e){
				System.out.println(e);
			}
			System.out.println(file.getName() + " Done!");
			//break;
		}
		
		long endTime = System.currentTimeMillis();
		long time = endTime - startTime;
		System.out.println("Time: " + time + "ms");
	}
	
	public static class iThread extends Thread{
		int index, passes, blurSize, start, end, imgWidth;
		static int percent = 0;
		static int oldP = 0;
		static int count = 0;
		
		public iThread(int index, int threads, int passes, int blurSize){
			this.index = index;
			this.passes = passes;
			this.blurSize = blurSize;
			//try{
			//	L.lock();
			this.imgWidth = img.getWidth();
			this.start = index * img.getHeight()/threads;
			this.end   = (index+1) * img.getHeight()/threads;
			//} finally{
			//	L.unlock();
			//}
		}
		
		public void run(){
			//System.out.println("Thread["+this.index+"] Start: "+this.start);
			//System.out.println("Thread["+this.index+"] End  : "+this.end);
			
			//Goal: For each pixel, get the average RGB value in a 25x25 px box
			//		and set it to that pixel.  Goes from left to right and then
			//		down between start and end pixels.
			int halfBlur = (this.blurSize-1)/2;
			int rStart,rEnd,cStart,cEnd;
			//For loops for one pixel
			//System.out.println("Start!");
			for(int y = this.start; y < this.end; y++){
				for(int x = 0; x < this.imgWidth; x++){
					//Calc start and end rows and columns
					//System.out.println("Thread["+this.index+"] X["+x+"] Y["+y+"]");
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
					int pixels = (rEnd-rStart)*(cEnd-cStart);
					int tmpR = 0;
					int tmpG = 0;
					int tmpB = 0;
					int RGB = 0;
					//For loops to get 25x25 px area
					for(int r = rStart; r < rEnd; r++){
						for(int c = cStart; c < cEnd; c++){
							//Grab RGB values
							//try{
							//	L.lock();
							RGB = img.getRGB(c,r);
							//} finally{
							//	L.unlock();
							//}
							tmpR +=((0x00ff0000 & RGB) >> 16);
							tmpG +=((0x0000ff00 & RGB) >> 8);
							tmpB +=((0x000000ff & RGB));
						}
					}
					tmpR = tmpR/pixels;
					tmpG = tmpG/pixels;
					tmpB = tmpB/pixels;
					//Set RGB value to new image
					try{
						L.lock();
						tmpImg.setRGB(x, y, new Color(tmpR,tmpG,tmpB).getRGB());
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
						
					} finally{
						L.unlock();
					}
				}
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