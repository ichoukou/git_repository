package native_agent;
import java.io.*;
import java.io.IOException;
public class execl_shell{
	
	public static String startret;
	public static String cmdret;
	public static Process pro;
	public static DataOutputStream output;
	public static BufferedReader input;
	public static DataInputStream error_input;
	public static Boolean can_su;
	public static String ndk_exe;
	
	public static String sttret;//tiaoshi

	public static void initData() {
		pro = null;
		can_su = null;
		ndk_exe = "/data/data/native";
		cmdret = "";
		//slnt_sokt = new Slnt_sokt();
		sttret = "";
	}

	public static boolean canSU() {
		if(can_su == null) {
			execl_shell_b.initData();
			//System.out.println("stjst");
			can_su = Boolean.valueOf(execl_shell_b.execute_su("id").contains("uid=0"));
		}
		return can_su.booleanValue();
	}
    
    public static boolean start_native(String port) {
		initData();
		if(!get_shell(true)) {
			return false;
		}
		MyThread t = new MyThread();
		t.start();
		return true;
	}
	
	/*public static boolean end_native() {
		run_command("endserver");
		try{
			Thread.currentThread().sleep(1000);
		}catch(InterruptedException ie){
			ie.printStackTrace();
		}
		return true;
	}*/
    
    public static boolean get_shell(boolean need_su) {
		try {
            Runtime runtime = Runtime.getRuntime();
            if(!canSU() && need_su)
            {
				System.out.println("your phone need root,so we can not exec su");
				
				return false;
			}
            pro = canSU() && need_su ? runtime.exec("su") : runtime.exec("su");
        }
        catch(Exception e) {
			return false;
        }

        output = new DataOutputStream(pro.getOutputStream());
        //System.out.println(pro.getInputStream());
        input = new BufferedReader(new InputStreamReader(pro.getInputStream()));
        error_input = new DataInputStream(pro.getErrorStream());
        return true;
	}
    
    public static String execute_shell(String[] commands) {
        String ret_string;
        String StdOut = "";
        String StdErr = "";
        try {
            int cmd_len = commands.length;
            int ing_len = 0;
            while( ing_len < cmd_len) {
                output.writeBytes(String.valueOf(commands[ing_len]) + "\n");
                output.flush();
                ++ing_len;
            }
            output.writeBytes("exit\n");
            output.flush();
            pro.waitFor();
            
            String tem = "";
            while((tem = input.readLine()) != null)
			{
				StdOut += (tem + "\n");
			}

            while(error_input.available() > 0) {
                StdErr = String.valueOf(StdErr) + error_input.readLine() + "\n";
            }

            if(StdOut != "")
				ret_string = StdOut;
			else
				ret_string = StdErr;
        }
        catch(Exception e) {
            ret_string = "IOException:" + e.toString();
        }
        startret = ret_string;
        //System.out.println(ret_string);
        return ret_string;
    }

	public static void run_command(String cmd) {
		cmdret = "";
		//System.out.println("run "+cmd);
		Clnt_sokt.out.write(cmd);
		Clnt_sokt.out.flush();
		//read data from server
		String str = "";
		while(true)
		{
			try{
				//System.out.println(Clnt_sokt.in);
				str = Clnt_sokt.in.readLine() +"\n";
				//System.out.println(str);
				cmdret += str;
				if(str.trim().endsWith("FAIL")||str.trim().endsWith("SUCCESS"))
					break;
				
			}catch(IOException e){
				break;
			}

		}
	}
}

class execl_shell_b{
	
	public static String StdErr;
	public static String StdOut;
	public static Boolean can_su;
	public static String ndk_exe;

	public static void initData() {
		can_su = null;
		StdOut = null;
		StdErr = null;
		ndk_exe = "/data/data/native";
	}

	public static boolean canSU() {
		if(can_su == null) {
			can_su = Boolean.valueOf(execute_su("id").contains("uid=0"));
		}
		return can_su.booleanValue();
	}

	public static String execute(String command) {
		return executeShell(new String[]{command}, false);
	}

	public static String execute(String[] commands) {
		return executeShell(commands, false);
	}
	
	public static String execute_su(String[] commands) {
		return executeShell(commands, true);
	}

	public static String execute_su(String command) {
		return executeShell(new String[]{command}, true);
	}
	
	public static String executeNDK(String params) {
		return execute_su(new String[]{"chmod 755 " + ndk_exe, String.valueOf(ndk_exe) + " " + params});
	}
	
	public static String executeShell(String[] commands, boolean need_su) {
        String ret_string;
        Process pro = null;
        StdOut = "";
        StdErr = "";
        try {
            Runtime runtime = Runtime.getRuntime();
            pro = need_su ? runtime.exec("su") : runtime.exec("su");
        }
        catch(Exception e) {
			return "root failed...";
        }

        DataOutputStream v2 = new DataOutputStream(pro.getOutputStream());
        DataInputStream v1 = new DataInputStream(pro.getInputStream());
        DataInputStream v0 = new DataInputStream(pro.getErrorStream());
        try {
            int cmd_len = commands.length;
            int ing_len = 0;
            while( ing_len < cmd_len) {
                v2.writeBytes(String.valueOf(commands[ing_len]) + "\n");
                v2.flush();
                ++ing_len;
            }
            v2.writeBytes("exit\n");
            v2.flush();
            pro.waitFor();
            while(v1.available() > 0) {
				StdOut = String.valueOf(StdOut) + v1.readLine() + "\n";
            }

            while(v0.available() > 0) {
                StdErr = String.valueOf(StdErr) + v0.readLine() + "\n";
            }

            v1.close();
            v2.close();
            v0.close();
            if(StdOut != "")
				ret_string = StdOut;
			else
				ret_string = StdErr;
        }
        catch(Exception e) {
            ret_string = "IOException:" + e.getMessage();
        }
        execl_shell.sttret = ret_string;
        //System.out.println("execlsu:"+ret_string);
        ret_string = "uid=0";
        return ret_string;
    }
}



class MyThread extends Thread
{
	public void run() {
		//System.out.println(execl_shell.ndk_exe + " start " + String.valueOf(Nat_conn.port));
		execl_shell.execute_shell(new String[]{"chmod 755 " + execl_shell.ndk_exe, execl_shell.ndk_exe + " start " + String.valueOf(Nat_conn.port)});
	} 
}

/*
class Receive_msg extends Thread {
	public void run() {
		//System.out.println("Receive_msg.run()");
		String str = "";
		while(true)
		{
			try{
				str += Clnt_sokt.in.readLine();
			}catch(IOException e){
				break;
			}

			if(str.trim().equals("MSG_OVER"))
			{
				break;
			}
		}
		System.out.println(str);
		System.out.println("Receive_msg.end()");
	}  
}  
*/
