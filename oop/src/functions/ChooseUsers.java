package functions;

import java.io.IOException;
import java.util.Scanner;

import static functions.RoleDelivery.deliverymanInputLgPw;
import static functions.RoleDirector.directorInputLgPw;
import static functions.RoleWorker.workerInputLgPw;

public class ChooseUsers {
    // Выбор Аккаунта
    public static String chooseUsers() throws IOException {
        Scanner sc = new Scanner(System.in);

        System.out.println("Выберите вашу специальность :");
        System.out.println("(1) Директор");
        System.out.println("(2) Работник");
        System.out.println("(3) Доставщик");
        do {
            System.out.print("Ваш выбор: ");
            String choose = sc.nextLine();
            System.out.println();
            switch (choose) {
                case "director":
                case "Director":
                case "1":
                    System.out.println("Добро пожаловать, Директор..");
                    System.out.println("Введите логин и пароль");
                    directorInputLgPw();
                    break;
                case "worker":
                case "Worker":
                case "2":
                    System.out.println("Добро пожаловать, Работник..");
                    System.out.println("Введите логин и пароль");
                    workerInputLgPw();
                    break;
                case "deliveryman":
                case "Deliveryman":
                case "3":
                    System.out.println("Добро пожаловать, Доставщик..");
                    System.out.println("Введите логин и пароль");
                    deliverymanInputLgPw();
                    break;
                default:
                    System.out.println("Кто ты воин?");
                    System.out.print("Желаете выйти[1] или повторить[0]?");
                    int ex = sc.nextInt();
                    if (ex == 0){
                        chooseUsers();
                    }
                    else if(ex == 1){
                        System.exit(0);
                    }
            }
            break;
        } while (true);
        return "";
    }
}
