import java.util.*;
import java.util.regex.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.lang.System;
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.nio.file.PathMatcher;
import java.awt.image.BufferedImage;
import java.io.*;

import javax.imageio.*;

class threads{

	static AtomicInteger numPix = new AtomicInteger(0);
	static Thread[] threadList;
	static myThread[] myList;
	static File[] files;
	
	public static void main(String[] args){
		long startTime = System.currentTimeMillis();
		Scanner scan = new Scanner(System.in);
		System.out.println("Enter a filename pattern: ");
		String pattern = scan.nextLine();
		
		if(pattern.contains(".")){
			pattern = pattern.substring(0, pattern.lastIndexOf('.'));
			System.out.println(pattern);
		}
		
		File dir = new File(System.getProperty("user.dir"));
		File[] files = dir.listFiles();
		File[] images = new File[files.length];
		int index = 0;
		for(File file : files){
			String filename = file.getName();
			if(filename.contains(".")){
				filename = filename.substring(0, filename.lastIndexOf('.'));
			}

			if(String.format(pattern, index).equals(filename)){
				images[index] = file;
				index++;
			}
		}
		
		for(File file : images){
			if(file!=null)
			System.out.println(file.getName());
		}
		
		
		//files = files(pattern);
		
//		System.out.println("Enter how many threads you want to use: ");
//		int numT = scan.nextInt();
		
//		for(File file : files){
//			System.out.println(file.toString());
//		}
//		
//		threadList = new Thread[numT];
//		myList = new myThread[numT];
		
//		//Create Threads and start them
//		for(int i = 0; i < numT; i++){
//			myList[i] = new myThread(i);
//			threadList[i] = new Thread(myList[i]);
//			threadList[i].start();
//		}
//		
//		//Joins threads
//		for(int i = 0; i < numT; i++){
//			try{
//				threadList[i].join();
//			} catch(InterruptedException e){
//				return;
//			}
//		}
//		
//		long endTime = System.currentTimeMillis();
//		long time = endTime - startTime;
//		System.out.println("Pixels: " + numPix.toString());
//		System.out.println("Time: " + time + "ms");
	}
	
	public static class myThread implements Runnable{
		int index = 0;
		public myThread(int index){
			this.index = index;
		}
		
		public int getIndex(){
			return index;
		}
		
		public void run(){
			try{
				BufferedImage img = ImageIO.read(files[index]);
				countPixels(img);
				index++;
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
	
	public static File[] files(final String p){
		String path = System.getProperty("user.dir");
		File dir = new File(path);
		
		return dir.listFiles(new FilenameFilter(){
			public boolean accept(File dir, String filename){
				return filename.matches(p);
			}
		});
	}
}