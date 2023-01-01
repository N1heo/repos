package functions;

import java.io.IOException;
import java.util.Scanner;

import static functions.DB.*;
import java.sql.ResultSet;

public class RoleDelivery {
    // Авторизация курьера
    public static void deliverymanInputLgPw() throws IOException {
        Scanner sc = new Scanner(System.in);

        do {
            System.out.print("Введите логин: ");
            String input_lg = sc.next();
            sc.nextLine();
            System.out.print("Введите пароль: ");
            String input_pw = sc.next();
            sc.nextLine();

            boolean haveInArray = FileReader.authorization(2, input_lg, input_pw);

            if (haveInArray) {
                System.out.println();
                System.out.println("Вы вошли успешно!");
                System.out.println();
                menu();
                break;
            } else {
                System.out.println("Попытайтесь снова.");
            }
        } while (true);
    }

    public static String menu() throws IOException {
        Scanner sc = new Scanner(System.in);

        System.out.println("Меню пользователя (Доставщик):");
        System.out.println("(1) Показать список заказанных товаров");
        System.out.println("(2) Показать доставленные товары");
        System.out.println("(3) Доставить");
        System.out.println("(4) Показать количество доставленных товаров");
        System.out.println("(5) Показать количество заказанных товаров");
        System.out.println("(6) Показать мой заработок ");
        System.out.println("(7) Выход");
        do {
            System.out.print("Ваш выбор: ");
            String choose = sc.nextLine();
            System.out.println();
            switch (choose) {
                case "1":
                    System.out.println("Список заказанных товаров: ");
                    System.out.println();
                    show_delivery(true);
                    menu();
                case "2":
                    System.out.println("Список доставленных товаров: ");
                    System.out.println();
                    show_delivered(true);
                    menu();
                case "3":
                    deliver();
                    menu();
                case "4":
                    num_delivered();
                    System.out.println();
                    menu();
                case "5":
                    num_ordered();
                    System.out.println();
                    menu();
                case "6":
                    fee();
                    System.out.println();
                    menu();
                case "7":
                    System.out.println();
                    System.out.println("Выход из системы...");
                    System.exit(0);
                default:
                    System.out.println("Ошибка ввода");
                    System.out.print("Желаете выйти[1] или повторить[0]?");
                    int ex = sc.nextInt();
                    if (ex == 0){
                        menu();
                    }
                    else if(ex == 1){
                        System.exit(0);
                    }
            }
            break;
        } while (true);
        return "";
    }

    public static void show_delivery(boolean bool) throws IOException{
        try {

            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery( "SELECT * FROM ORDERED;" );

            System.out.format("%4s %-20s %7s %-50s", "id", "name", "amount", "category");
            System.out.println();
            while ( rs.next() ) {
                int id = rs.getInt("id");
                String  name = rs.getString("name");
                int amount  = rs.getInt("amount");
                String  category = rs.getString("category");
                System.out.format("%4s %-20s %7s %-50s", id, name, amount, category);    
                System.out.println();
           }
            rs.close();
            stmt.close();
        } catch ( Exception e ) {
            System.err.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
        System.out.println();
        if (bool){
            System.out.println("Таблица открыта успешно!");
        }
    }

    public static void show_delivered(boolean bool) throws IOException{
        try {
            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery( "SELECT * FROM PRODUCT;" );

            System.out.format("%4s %-30s %7s %-50s", "id", "name", "amount", "category");
            System.out.println();
            while ( rs.next() ) {
                int id = rs.getInt("id");
                String  name = rs.getString("name");
                int amount  = rs.getInt("amount");
                String  category = rs.getString("category");
                System.out.format("%4s %-30s %7s %-50s", id, name, amount, category);    
                System.out.println();
            }
            rs.close();
            stmt.close();
        } catch ( Exception e ) {
            System.err.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
        System.out.println();
        if (bool) {
            System.out.println("Таблица открыта успешно!");
        }
        
    }

    public static void deliver() throws IOException{
        try {
            System.out.println("Список заказанных товаров: ");
            System.out.println();
            show_delivery(false);
            System.out.println();

            Scanner sc = new Scanner(System.in);
            int delete_id;
            do {
                System.out.println("Введите id товара, который вы хотели бы доставить: ");
                while(!sc.hasNextInt()){
                    System.out.println("Ошибка ввода.. Повторите ещё раз: ");
                    sc.next();
                }
                delete_id = sc.nextInt();
            } while (delete_id <= 0);

            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery( "SELECT * FROM ORDERED WHERE ID = " + delete_id + ";");
            rs.next();
            String  name = rs.getString("name");
            double price = rs.getInt("price");
            int amount  = rs.getInt("amount");
            String  category = rs.getString("category");

            String sql = "DELETE from ORDERED where ID = " + delete_id + ";";
            stmt.executeUpdate(sql);

            sql = "INSERT INTO PRODUCT (NAME, PRICE, AMOUNT, CATEGORY)" 
                          + "VALUES ('"+ name + "', " + price + ", " +  amount + ", '" + category + "' );";  
            stmt.executeUpdate(sql);
            c.commit();

            System.out.println("Список доставленных товаров: ");
            System.out.println();
            show_delivered(false);
            
            rs.close();
            stmt.close();
        } catch (Exception e) {
            System.err.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
        System.out.println("Товар доставлен успешно!");
        System.out.println();
    }

    public static void num_delivered() throws IOException{
        try{
            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery( "SELECT * FROM PRODUCT;");
            int c = 0;
            while(rs.next()){
                c++;
            }
            System.out.println("Кол-во доставленных товаров - " + c);    
        } catch (Exception e) {
            System.err.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
    }

    public static void num_ordered() throws IOException{
        try{
            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery( "SELECT * FROM ORDERED;");
            int c = 0;
            while(rs.next()){
                c++;
            }
            System.out.println("Кол-во заказанных товаров - " + c);    
        } catch (Exception e) {
            System.err.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
    }

    public static void fee() throws IOException{
        try{
            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery( "SELECT order_fee FROM product;");
            double fee = 0;
            while(rs.next()){
                fee += rs.getDouble("order_fee");
            }

            System.out.println("Ваш заработок - " + fee);
        } catch (Exception e) {
            System.err.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
    }

}
