package functions;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class FileReader {
    public static boolean authorization(int n, String loginUser, String passwordUser) {
        try{
            String line = Files.readAllLines(Paths.get("logins_passwords.txt")).get(n);
            String [] log_pas = line.split(" ");
            String login = log_pas[0];
            String password = log_pas[1];
            if (loginUser.equals(login) && passwordUser.equals(password)){
                return true;
            }else {
                return false;
            }
        }
        catch(IOException e){
            System.out.println(e);
        }
        return true;
    }
}
