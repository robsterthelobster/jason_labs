import java.util.*;
import java.util.regex.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.lang.System;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import javax.imageio.*;

class threads{

	static AtomicInteger numPix = new AtomicInteger(0);
	static Thread[] threadList;
	static myThread[] myList;
	static File[] allFiles;
	static int numT;
	
	public static void main(String[] args){
		Scanner scan = new Scanner(System.in);
		System.out.println("Enter a filename pattern: ");
		String pattern = scan.nextLine();
		//String pattern = "frame0000 - Copy (%02d).png";
		
		System.out.println("Enter how many threads you want to use: ");
		numT = scan.nextInt();
		//numT = 4;

		long startTime = System.currentTimeMillis();
		
		threadList = new Thread[numT];
		myList = new myThread[numT];
		
		allFiles = getFiles(pattern);
		
		//Create Threads and start them
		for(int i = 0; i < numT; i++){
			myList[i] = new myThread(i);
			threadList[i] = new Thread(myList[i]);
			threadList[i].start();
		}
		
		//Joins threads
		for(int i = 0; i < numT; i++){
			try{
				threadList[i].join();
			} catch(InterruptedException e){
				return;
			}
		}
		
		long endTime = System.currentTimeMillis();
		long time = endTime - startTime;
		System.out.println("Pixels: " + numPix.toString());
		System.out.println("Time: " + time + "ms");
	}
	
	public static class myThread implements Runnable{
		int index = 0;
		public myThread(int index){
			this.index = index;
		}
		
		private int getIndex(){
			return index;
		}
		
		public void run(){
			try{
				for(int i = this.index; i < allFiles.length; i += numT){
					BufferedImage img = ImageIO.read(allFiles[i]);
					countPixels(img);
				}
			} catch (IOException e){
				e.printStackTrace();
			}
		}
	}
	
	public static void countPixels(BufferedImage img){
		for(int y = 0; y < img.getHeight(); y++){
			for(int x = 0; x < img.getWidth(); x++){
				int RGB = img.getRGB(x,y);
				int r = (0x00ff0000 & RGB) >> 16;
				int g = (0x0000ff00 & RGB) >> 8;
				int b = (0x000000ff & RGB);
				if (r == 255 && g == 255 && b == 255)
					numPix.incrementAndGet();
			}
		}
	}
	
	public static File[] getFiles(String pattern){
		File dir = new File(System.getProperty("user.dir"));
		File[] files = dir.listFiles();
		File[] temp = new File[files.length];
		int index = 0;
		for(File file: files){
			String filename = file.getName();
			if(String.format(pattern, index).equals(filename)){
				temp[index] = file;
				index++;
			}
		}
		File[] images = new File[index];
		for (int i = 0; i < images.length; i++){
			images[i] = temp[i];
		}
		return images;
	}
}