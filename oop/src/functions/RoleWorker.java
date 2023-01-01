package functions;

import java.io.IOException;
import java.util.Scanner;

import static functions.DB.*;
import static functions.RoleDelivery.show_delivery;
import java.sql.ResultSet;

public class RoleWorker {
    // Авторизация работника
    public static void workerInputLgPw() throws IOException {
        Scanner sc = new Scanner(System.in);

        do {
            System.out.print("Введите логин: ");
            String input_lg = sc.next();
            sc.nextLine();
            System.out.print("Введите пароль: ");
            String input_pw = sc.next();
            sc.nextLine();

            boolean haveInArray = FileReader.authorization(1, input_lg, input_pw);

            if (haveInArray) {
                System.out.println("Работник, вы успешно вошли!");
                menu();

                break;
            } else {
                System.out.println("Попытайтесь снова");
            }
        } while (true);
    }

    public static String menu() throws IOException {
        Scanner sc = new Scanner(System.in);

        System.out.println();
        System.out.println("Меню пользователя (Работник):");
        System.out.println("(1) Показать весь список товаров доступных в магазине");
        System.out.println("(2) Искать товар: ");
        System.out.println("(3) Показать отчёт");
        System.out.println("(4) Выполнить заказ");
        System.out.println("(5) Показать список заказанных товаров");
        System.out.println("(6) Показать отсутсвующие на складе товары ");
        System.out.println("(7) Показать все товары, на которые действует скидка");
        System.out.println("(8) Удалить заказ");
        System.out.println("(9) Поставить скидку");
        System.out.println("(10) Выход");
        do {
            System.out.print("Ваш выбор: ");
            String choose = sc.nextLine();
            System.out.println();
            switch (choose) {
                case "1":
                    System.out.println("Cписок товаров доступных в магазине: ");
                    System.out.println();
                    show_all_product(true);
                    menu();
                case "2":
                    search_product();
                    menu();
                case "3":
                    System.out.println("Отчёт: ");
                    System.out.println();
                    report();
                    menu();
                case "4":
                    order();
                    menu();
                case "5":
                    System.out.println("Список заказанных товаров: ");
                    System.out.println();
                    show_delivery(true);
                    menu();
                case "6":
                    System.out.println("Отсутсвующие на складе товары: ");
                    System.out.println();
                    show_missing();
                    menu();
                case "7":
                    System.out.println("Все товары, на которые действует скидка: ");
                    System.out.println();
                    show_sales();
                    menu();
                case "8":
                    System.out.println("Список заказанных товаров: ");
                    System.out.println();
                    show_delivery(false);
                    int delete_id;
                    do {
                        System.out.println("Введите ID товара для удаления: ");
                        while (!sc.hasNextInt()) {
                            System.out.println("Ошибка ввода.. Повторите ещё раз: ");
                            sc.next();
                        }
                        delete_id = sc.nextInt();
                    } while (delete_id <= 0);
                    delete_order(delete_id);
                    menu();
                case "9":
                    System.out.println("Cписок товаров доступных в магазине: ");
                    System.out.println();
                    show_all_product(false);
                    int sale_id;
                    do {
                        System.out.println("Введите ID товара для скидки: ");
                        while (!sc.hasNextInt()) {
                            System.out.println("Ошибка ввода.. Повторите ещё раз: ");
                            sc.next();
                        }
                        sale_id = sc.nextInt();
                    } while (sale_id <= 0);

                    double sale_amount;
                    do {
                        System.out.println("Введите скидку, в дробном виде(0.1, 0.5): ");
                        while (!sc.hasNextDouble()) {
                            System.out.println("Ошибка ввода.. Повторите ещё раз: ");
                            sc.next();
                        }
                        sale_amount = sc.nextDouble();
                    } while (sale_id <= 0);

                    make_sale(sale_amount, sale_id);
                    menu();
                case "10":
                    System.out.println("Выход из системы");
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

    public static void show_all_product(boolean bool) throws IOException{
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
        if (bool){
            System.out.println("Таблица открыта успешно!");
        }
    }

    public static String search_product() throws IOException{
        Scanner sc = new Scanner(System.in, "cp866");

        System.out.println("Искать товар:");
        System.out.println("(1) По серийному номеру");
        System.out.println("(2) По названию");
        do {
            System.out.print("Ваш выбор: ");
            String choose = sc.nextLine();
            switch (choose) {
                case "1":
                    int value;
                    do{
                        System.out.println("Напишите серийный номер для поиска:>>");
                        while(!sc.hasNextInt()){
                            System.out.println("Ошибка ввода.. Повторите ещё раз:>>");
                            sc.next();
                        }
                        value = sc.nextInt();
                    } while (value <= 0);
                    System.out.println();
                    System.out.println("Рез-ты поиска:");
                    finder("ID", Integer.toString(value));
                    break;
                case "2":
                    System.out.println("Напишите имя товара для поиска:>>");
                    String value2 = sc.nextLine();
                    System.out.println();
                    System.out.println("Рез-ты поиска:");
                    finder("NAME", value2);
                    break;
                default:
                    System.out.println("Ошибка ввода");
                    System.out.print("Желаете выйти[1] или повторить[0]?");
                    int ex = sc.nextInt();
                    if (ex == 0){
                        search_product();
                    }
                    else if(ex == 1){
                        System.exit(0);
                    }
            }    
            break;

        } while (true);
        return "";
    }

    public static void finder(String id_or_name, String value) throws IOException{
        try {
            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery( "SELECT * FROM PRODUCT WHERE " + id_or_name + " = '" + value + "';" );

            if (rs.next() == false){
                System.out.println("Товар не найден!");
            } else{
                
                System.out.format("%4s %-30s %13s %7s %-50s", "id", "name", "price", "amount", "category");
                System.out.println();
                do{
                    int id = rs.getInt("id");
                    String  name = rs.getString("name");
                    double price = rs.getDouble("price");
                    int amount  = rs.getInt("amount");
                    String category = rs.getString("category");
                    System.out.format("%4s %-30s %13s %7s %-50s", id, name, price, amount, category);
                    System.out.println();
                } while ( rs.next()); 
                rs.close();
                stmt.close();
                System.out.println();
                System.out.println("Товар найден успешно!");
            }
        } catch ( Exception e ) {
            System.err.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
    }
    
    public static void report() throws IOException{
        try {
            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery( "SELECT * FROM PRODUCT;" );

            System.out.format("%4s %-30s %7s %-50s %4s", "id", "name", "amount", "category", "year");
            System.out.println();
            while ( rs.next() ) {
                int id = rs.getInt("id");
                String  name = rs.getString("name");
                int amount  = rs.getInt("amount");
                String category = rs.getString("category");
                String time = rs.getString("buy_date");
                String [] parts = time.split("-");
                String year = parts[0];
                System.out.format("%4s %-30s %7s %-50s %4s", id, name, amount, category, year);    
                System.out.println();
            }
            rs.close();
            stmt.close();
        } catch ( Exception e ) {
            System.err.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
        System.out.println();
        System.out.println("Таблица открыта успешно!");
    }


    public static String order() throws IOException{
        Scanner sc = new Scanner(System.in, "cp866");

        System.out.println("Заказать товар:");
        System.out.println("(1) Заказать новый");
        System.out.println("(2) Докупить товар");
        do {
            System.out.print("Ваш выбор: ");
            String choose = sc.nextLine();
            switch (choose) {
                case "1":
                    order_new();
                    break;
                case "2":
                    show_all_product(false);
                    System.out.println();
                    System.out.println("Введите имя товара, требуемого для докупки: ");
                    String order_name = sc.nextLine();
                    System.out.println("Введите кол-во товара для докупки: ");
                    int buy_amount = sc.nextInt();
                    order_old(order_name, buy_amount);
                    
                    break;
                default:
                    System.out.println("Ошибка ввода");
                    System.out.print("Желаете выйти[1] или повторить[0]?");
                    int ex = sc.nextInt();
                    if (ex == 0){
                        search_product();
                    }
                    else if(ex == 1){
                        System.exit(0);
                    }
            }    
            break;

        } while (true);
        return "";
    }

    public static void order_new() throws IOException {
        try{
            Scanner sc = new Scanner(System.in, "cp866");
            System.out.println("Для заказа нового товара, нужно также внести запись о нём: ");
            System.out.println("Введите имя товара: ");
            String name = sc.nextLine();
            double price;
            do{
                System.out.println("Введите цену товара: ");
                while (!sc.hasNextDouble()){
                    System.out.println("Ошибка ввода.. Повторите ещё раз: ");
                    sc.next();
                }
                price = sc.nextDouble();
            } while (price <= 0);
            
            int amount;
            do{
                System.out.println("Сколько бы вы хотели заказать?: ");
                while (!sc.hasNextInt()){
                    System.out.println("Ошибка ввода.. Повторите ещё раз: ");
                }
                amount = sc.nextInt();
            } while (amount <= 0);

            System.out.println("Введите категорию товара: ");
            sc.nextLine();
            String category = sc.nextLine();

            stmt = c.createStatement();
            String sql = "INSERT INTO ORDERED (NAME, PRICE, AMOUNT, CATEGORY) "
                          + "VALUES ('" + name + "'," + price + "," + amount + ",'" + category + "');";
            stmt.executeUpdate(sql);
            stmt.close();
            c.commit();

        } catch (Exception e) {
            System.err.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
        System.out.println();
        System.out.println("Товар заказан успешно!");
    }

    public static void order_old(String order_name, int buy_amount) throws IOException {
        try {
            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery( "SELECT EXISTS(SELECT 1 FROM ordered WHERE name = '" + order_name + "')");
            rs.next();
            boolean bool = rs.getBoolean("exists");

            if(bool){
                String sql = "UPDATE ordered SET amount = amount + "+ buy_amount +" where name = '"+ order_name +"';";
                stmt.executeUpdate(sql);
                c.commit();
            } else{
                rs = stmt.executeQuery( "SELECT * FROM product WHERE name = '" + order_name + "';");
                rs.next();
                String name = rs.getString("name");
                double price = rs.getInt("price");
                int amount  = buy_amount;
                String category = rs.getString("category");

                String sql2 = "INSERT INTO ORDERED (NAME, PRICE, AMOUNT, CATEGORY)" 
                               + "VALUES ('"+ name + "', " + price + ", " +  amount + ", '" + category + "' );";  
                stmt.executeUpdate(sql2);
                c.commit();
            }

            rs.close();
            stmt.close();
        } catch (Exception e) {
            System.err.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
        System.out.println("Товар заказан успешно!");
        System.out.println();
        
    }

    public static void show_missing() throws IOException{
        try {
            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery( "SELECT * FROM PRODUCT WHERE amount = 0;" );

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
        System.out.println("Таблица открыта успешно!");
    }

    public static void show_sales() throws IOException{
        try {
            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery( "SELECT * FROM product WHERE sale = true;" );

            System.out.format("%4s %-30s %7s %11s %-50s", "id", "name", "amount", "sale_amount", "category");
            System.out.println();
            while ( rs.next() ) {
                int id = rs.getInt("id");
                String  name = rs.getString("name");
                int amount  = rs.getInt("amount");
                double sale_amount = rs.getDouble("sale_amount");
                String sale_amount_percentage =Long.toString(Math.round(sale_amount*100))+"%";
                String  category = rs.getString("category");
                System.out.format("%4s %-30s %7s %11s %-50s", id, name, amount, sale_amount_percentage, category);    
                System.out.println();
            }
            rs.close();
            stmt.close();
        } catch ( Exception e ) {
            System.err.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
        System.out.println();
        System.out.println("Таблица открыта успешно!");
    }


    public static void delete_order(int delete_id) throws IOException{
        try {
            stmt = c.createStatement();
            String sql = "DELETE FROM ordered WHERE id = "+ delete_id +";";
            stmt.executeUpdate(sql);
            c.commit();

            stmt.close();
        } catch ( Exception e ) {
            System.err.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
        System.out.println("Заказ удалён!");
    }

    public static void make_sale(double sale_amount, int sale_id) throws IOException{
        try{
            stmt = c.createStatement();
            String sql = "UPDATE product SET sale_amount = "+ sale_amount +"where ID =" + sale_id + ";";
            stmt.executeUpdate(sql);
            c.commit();

            stmt.close();
        } catch ( Exception e ) {
            System.err.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
        System.out.println();
        System.out.println("Скидка поставлена успешно!");
    }
}
