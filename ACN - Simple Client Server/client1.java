package my_project;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

public class client1 {

	public static void main(String[] args) 
	{
		try
		{
			Socket s2 = new Socket("localhost",9999);
			DataInputStream dis = new DataInputStream(s2.getInputStream());
			DataOutputStream dos = new DataOutputStream(s2.getOutputStream());
			BufferedReader buffer_reader = new BufferedReader(new InputStreamReader(System.in));
			
			String str1="", str2="";
			while(!str1.equals("stop"))
			{
				System.out.println("Client:");
				str1 = buffer_reader.readLine();
				dos.writeUTF(str1);
				dos.flush();
				str2 = dis.readUTF();
				System.out.println("Server:"+str2);
			}
			
			dis.close();
			dos.close();
			s2.close();
		}
		catch (IOException e1)
		{
			e1.printStackTrace();
		}
	}
}