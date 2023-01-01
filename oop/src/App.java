import java.io.IOException;

import static functions.ChooseUsers.chooseUsers;
import static functions.DB.open_db;
import static functions.DB.create_table;

public class App {
    public static void main(String args[]) throws IOException {
        open_db();
        create_table();
        
        System.out.println("Чтобы начать работу, пожалуйста, авторизуйтесь..");
        chooseUsers();
    }
}
