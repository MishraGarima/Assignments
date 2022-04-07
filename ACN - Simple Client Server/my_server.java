package my_project;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

public class my_server {

	public static void main(String[] args) 
	{
		try 
		{
			ServerSocket server_socket = new ServerSocket(9999);
			Socket s1 = server_socket.accept();
			DataInputStream dis = new DataInputStream(s1.getInputStream());
			DataOutputStream dos = new DataOutputStream(s1.getOutputStream());
			BufferedReader buffer_reader = new BufferedReader(new InputStreamReader(System.in));
			
			String str1="", str2="";
			while(!str1.equals("stop"))
			{
				str1 = dis.readUTF();
				System.out.println("Client:"+str1);
				System.out.println("Server:");
				str2 = buffer_reader.readLine();
				dos.writeUTF(str2);
				dos.flush();
			}
			
			dis.close();
			dos.close();
			s1.close();
			server_socket.close();
		}
		catch (IOException e1)
		{
			e1.printStackTrace();
		}	
	}
}