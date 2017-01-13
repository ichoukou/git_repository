package native_agent;
import java.net.*;
import java.io.*;

public class Clnt_sokt {
	
	public static Socket client;
	public static BufferedReader in;
	public static PrintWriter out;
	
	public static int init_client_sokt(int port)
	{	
		try{
			client = new Socket(InetAddress.getLocalHost(),port);
			//System.out.println(client.getInputStream());
			//SocketAddress remoteAddr=new InetSocketAddress(InetAddress.getLocalHost(),port);
			in = new BufferedReader(new InputStreamReader(client.getInputStream()));
			out = new PrintWriter(client.getOutputStream());
			//wait build connect for 1 minite
			//client.connect(remoteAddr, 30000);
		}catch(Exception e) {
			//System.out.println(e.toString());
			return -1;
		}
		return 0;
		
	}
	
	public static boolean isPortUsing(String host,int port) throws UnknownHostException
	{  
        boolean flag = false;  
        InetAddress theAddress = InetAddress.getByName(host);  
        try 
        {  
            Socket socket = new Socket(theAddress,port);  
            flag = true;  
        } catch (IOException e) {  
           
        }  
        return flag;  
    }  
    
    public static boolean isLoclePortUsing(int port)
    {  
        boolean flag = true;  
        try 
        {  
            flag = isPortUsing("127.0.0.1", port);  
        } catch (Exception e) 
        {  
        }  
        return flag;  
    }  
    
    public static boolean isConnected(Socket socket)
    {
		boolean isconnect = true;
		try{
			socket.sendUrgentData(0xFF);
		}catch(Exception ex){
			isconnect = false;
		}
		return isconnect;
	}
	
	public static boolean close_client_sokt()
	{
		try{
			in.close();
			out.close();
			client.close();
		}catch(Exception e) {
			return false;
		}
		return true;
	}
}

