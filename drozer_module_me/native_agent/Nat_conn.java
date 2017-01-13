package native_agent;
import java.io.*;
import java.io.IOException;

public class Nat_conn
{  
	public static int port;//record port server need to start,and client need to connect
	
	public static void initData(String port1)
	{
		port = Integer.valueOf(port1);
		execl_shell.initData();
	}
	
	public static String start_native() // once start programe native success, to init client,open a port to connect native
	{
		String retstart = "START_FAIL";
		if(execl_shell.start_native(String.valueOf(port))==false)
			return retstart;//+execl_shell.sttret;
		//execl_shell.start_native(String.valueOf(port));
		try{
			Thread.currentThread().sleep(1000);
		}catch(InterruptedException ie){
			ie.printStackTrace();
		}
		if(Clnt_sokt.init_client_sokt(port)== -1)
		{
			//System.out.println(execl_shell.startret);
			return retstart;//"2"+retstart+execl_shell.sttret;
		}
		retstart = "";
		while(true)
		{
			String str = "";
			try{
				
				str = Clnt_sokt.in.readLine();
				retstart += str;
				if(str.trim().endsWith("SUCCESS")||str.trim().endsWith("FAIL"))
					break;
				
			}catch(IOException e){
				break;
			}
		}
		if(!retstart.equals("CLIENT_CONNECT_SUCCESS"))
		{
			retstart = "START_FAIL";
			return retstart;//+execl_shell.sttret;
		}
		//System.out.println(retstart);
		return retstart;//+execl_shell.sttret;
	}

	public static String end_native()
	{
		/*execl_shell.run_command("endserver");
		if(!execl_shell.cmdret.contains("ENDSERVER_SUCCESS"))
		{
			return "ENDSERVER_FAIL";
		}
		Clnt_sokt.close_client_sokt();
		return "ENDSERVER_SUCCESS";*/
		execl_shell.run_command("endserver");
		return execl_shell.cmdret;
	}
	
	
	public static String run_command(String cmd) 
	{
		String cmd_ret = "COMMAND_FAIL";
		if(!Clnt_sokt.isLoclePortUsing(port))
		{
			if(start_native() == "START_FAIL")
				return cmd_ret;
		}
		if(!Clnt_sokt.isConnected(Clnt_sokt.client))
		{
			if(Clnt_sokt.init_client_sokt(port) == -1)
				return cmd_ret;
		}
		execl_shell.run_command(cmd);
		//System.out.println(execl_shell.cmdret);
		return execl_shell.cmdret;
	}
	
	
	public static void main(String args[]) {
		initData(args[0]);
		String s = start_native();
		if(s.equals("START_FAIL"))
			return ;
		System.out.println(s);
		//System.out.println(end_native());
		for(int i = 0; i<10; i++)
		{
			try{
				BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
				String ss = br.readLine();
				System.out.println(i+":"+run_command(ss));
			}catch(Exception e){}
			
		}
		System.out.println(end_native());
		return ;
	}
}
