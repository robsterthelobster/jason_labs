import javax.sound.sampled.*;
import java.net.*;
import java.util.*;
import java.io.*;

//java media arsenic.ssucet.org 55555 [station] 
//^ plays station

//java media    or    java media arsenic.ssucet.org 55555
//^displays stations

public class media{

	public static void main(String[] args){
		int size = 65535;
		String password = "gimmeh mah tunes";
		String server;
		int port;
		String station = null;
		
		if(args.length > 0){
			server = args[0];
			port = Integer.parseInt(args[1]);
			if(args.length >= 3)
				station = args[2];
		} else{
			server = "arsenic.ssucet.org";
			port = 55555;
		}
		
		String input = password + "+";
		if(station != null)
			input += station;
		
		try{
			DatagramSocket s = new DatagramSocket();
			InetAddress ip = InetAddress.getByName(server);
			s.send(new DatagramPacket(input.getBytes(), input.length(), ip, port));
			DatagramPacket d = new DatagramPacket(new byte[size], size);
			s.receive(d);
			
			//Get stations
			if(station == null){
				byte[] tmp = d.getData();
				if(tmp.length > 0){
					String str = new String(tmp);
					JSONParser jp = new JSONParser();
					Object test = jp.parse(str);
					System.out.println("Data Received: " + test);
				} else{
					System.out.println("No Data Received!");
				}
			//Get stream data
			} else{
				byte[] data = d.getData();
				String paramStr = new String(data);
				int f = paramStr.indexOf("{");
				int l = paramStr.lastIndexOf("}");
				paramStr = paramStr.substring(f+1,l);
				Scanner scan = new Scanner(paramStr);
				//System.out.println(paramStr);
				
				int rate = 0;
				int bytespersample = 0;
				int channels = 0;
				boolean is_signed = false;
				
				while(true){
					String tmp = scan.next();
					//System.out.println(tmp);
					if(tmp.matches("\"samplespersecond\":")){
						tmp = scan.next();
						rate = Integer.parseInt(tmp.substring(0,tmp.length()-1));
					}else if(tmp.matches("\"bytespersample\":")){
						tmp = scan.next();
						bytespersample = Integer.parseInt(tmp.substring(0,tmp.length()-1));
					}else if(tmp.matches("\"channels\":")){
						tmp = scan.next();
						channels = Integer.parseInt(tmp.substring(0,tmp.length()-1));
					}else if(tmp.matches("\"signed\":")){
						tmp = scan.next();
						is_signed = Boolean.valueOf(tmp);
					}
					if(!scan.hasNext())
						break;
				}
				
				System.out.println("Rate: " + rate);
				System.out.println("Bytespersample: " + bytespersample);
				System.out.println("Channels: " + channels);
				System.out.println("Is_signed: " + is_signed);
			
				//Play music
				try{
					System.out.println("Playing...");
					int offset = 0;
					if(!input.endsWith("!"))
						input += "!";
					while(true){
						//Since server cuts out around 15 seconds, resend data to be active
						s.send(new DatagramPacket(input.getBytes(), input.length(), ip, port));
	
						DatagramPacket d2 = new DatagramPacket(new byte[size], size);
						s.receive(d2);
						AudioFormat dfmt = new AudioFormat(rate, bytespersample*8, channels, is_signed, false);
						SourceDataLine speaker = AudioSystem.getSourceDataLine(dfmt);
						speaker.open(dfmt);
						speaker.start();
					
						byte[] mdata = d2.getData();
						speaker.write(mdata,offset,d2.getLength());
					}
				} catch(LineUnavailableException e){
					System.out.println(e);
				}
			}
		} catch (SocketException e){
			System.out.println(e);
		} catch (UnknownHostException e){
			System.out.println(e);
		} catch (IOException e){
			System.out.println(e);
		}
		System.out.println("Done!");
	}
}