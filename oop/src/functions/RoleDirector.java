package functions;

import java.io.IOException;
import java.sql.ResultSet;
import java.util.Scanner;

import static functions.RoleWorker.show_all_product;
import static functions.RoleWorker.report;
import static functions.DB.*;

public class RoleDirector {
     // Авторизация директора
     public static void directorInputLgPw() throws IOException {
        Scanner sc = new Scanner(System.in);

        do {
            System.out.print("Введите логин: ");
            String input_lg = sc.next();
            sc.nextLine();
            System.out.print("Введите пароль: ");
            String input_pw = sc.next();
            sc.nextLine();

            boolean haveInArray = FileReader.authorization(0, input_lg, input_pw);
            
            if (haveInArray) {
                System.out.println();
                System.out.println("Директор, вы успешно вошли!");
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
        System.out.println("Меню пользователя (Директор):");
        System.out.println("(1) Показать список всех товаров");
        System.out.println("(2) Показать количество товаров");
        System.out.println("(3) Показать товар с максимальным количеством");
        System.out.println("(4) Показать товар с минимальным количеством");
        System.out.println("(5) Показать отчёт по закупкам товаров");
        System.out.println("(6) Выход");
        do {
            System.out.print("Ваш выбор: ");
            String choose = sc.nextLine();
            System.out.println();
            switch (choose) {
                case "1":
                    System.out.println("Cписок товаров доступных в магазине:");
                    System.out.println();
                    show_all_product(true);
                    menu();
                case "2":
                    System.out.println("Таблица кол-ва товаров по категориям: ");
                    System.out.println();
                    amount_by_category();
                    menu();
                case "3":
                    System.out.println("Товар(-ы) с максимальным кол-вом: ");
                    System.out.println();
                    max_min("MAX");
                    menu();
                case "4":
                    System.out.println("Товар(-ы) с минимальным кол-вом: ");
                    System.out.println();
                    max_min("MIN");
                    menu();
                case "5":
                    System.out.println("Отчёт по закупкам товаров: ");
                    System.out.println();
                    report();
                    menu();
                case "6":
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

    public static void amount_by_category() throws IOException{
        try{
            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery( "SELECT category, count(*) AS amount FROM product GROUP BY 1;");
            System.out.format("%-30s %5s", "category", "amount");
            System.out.println();
            while ( rs.next() ) {
                String category = rs.getString("category");
                int amount = rs.getInt("amount");
                System.out.format("%-30s %5s", category, amount);
                System.out.println();
            }
        } catch (Exception e) {
            System.out.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
        System.out.println();
        System.out.println("Кол-во посчитано успешно!");
    }

    public static void max_min(String max_or_min) throws IOException{
        try{
            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery( "SELECT * FROM (SELECT name as product_name, amount as amount FROM product)"
                            + "AS m_table WHERE amount = (SELECT "+ max_or_min +"(amount) FROM product WHERE amount !=0);");
            System.out.format("%-30s %6s", "product_name", "amount");
            System.out.println();
            while ( rs.next() ) {
                String product_name = rs.getString("product_name");
                int amount = rs.getInt("amount");
                System.out.format("%-30s %6s", product_name, amount);
                System.out.println();
            }
        } catch (Exception e) {
            System.out.println( e.getClass().getName()+": "+ e.getMessage() );
            System.exit(0);
        }
    }

}
