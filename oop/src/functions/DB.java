package functions;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class DB {

   static Connection c;
   static Statement stmt;

   public DB(){
      c = null;
      stmt = null;
   }

   public static void open_db() {
      try {
         Class.forName("org.postgresql.Driver");
         c = DriverManager
            .getConnection("jdbc:postgresql://localhost:5432/db_oop",
            "postgres", "iruves45");
         c.setAutoCommit(false);
      } catch (Exception e) {
         e.printStackTrace();
         System.err.println(e.getClass().getName()+": "+e.getMessage());
         System.exit(0);
      }
      System.out.println("Открывается база данных....");
   }

   public static void create_table() {
      try {
         stmt = c.createStatement();
         String sql = "CREATE TABLE IF NOT EXISTS PRODUCT " +
            "(ID            SERIAL            PRIMARY KEY," +
            " NAME          TEXT              NOT NULL, " +
            " PRICE         DOUBLE PRECISION  NOT NULL, " +
            " AMOUNT        INT, " +
            " CATEGORY      TEXT              NOT NULL, " +
            " SALE          BOOLEAN           NOT NULL DEFAULT FALSE, " +
            " SALE_AMOUNT   DOUBLE PRECISION  NOT NULL DEFAULT 0, " +
            " ORDER_FEE     DOUBLE PRECISION, " +
            " BUY_DATE      TIMESTAMP         DEFAULT NOW())";
         stmt.executeUpdate(sql);

         sql = "CREATE TABLE IF NOT EXISTS ORDERED " +
            "(ID            SERIAL            PRIMARY KEY," +
            " NAME          TEXT              NOT NULL, " +
            " PRICE         DOUBLE PRECISION  NOT NULL, " +
            " AMOUNT        INT, " +
            " CATEGORY      TEXT              NOT NULL, " +
            " ORDER_DATE    TIMESTAMP         DEFAULT NOW())";
         stmt.executeUpdate(sql);

         sql = " CREATE OR REPLACE FUNCTION SET_DEFAULT_FEE() RETURNS TRIGGER AS $$ " +
                        " BEGIN " +
                        "   IF NEW.ORDER_FEE IS NULL THEN " + 
                        "      NEW.ORDER_FEE := NEW.PRICE * NEW.AMOUNT * 0.1; " +
                        "   END IF; " +
                        "   RETURN NEW; "+
                        "END; " +
                        "$$ LANGUAGE PLPGSQL; " +

                        "DROP TRIGGER IF EXISTS TRIG_SET_DEFAULT_FEE " +
                        "ON PUBLIC.PRODUCT;" +

                        "CREATE TRIGGER TRIG_SET_DEFAULT_FEE " +
                        " BEFORE INSERT " +
                        " ON PRODUCT " +
                        " FOR EACH ROW " +
                        " EXECUTE PROCEDURE SET_DEFAULT_FEE();";
         stmt.executeUpdate(sql);

         sql = " CREATE OR REPLACE FUNCTION set_sale_bool() RETURNS TRIGGER AS $$ " +
                        " BEGIN " +
                        "   IF NEW.sale_amount > 0 THEN " + 
                        "      NEW.sale := TRUE; " +
                        "   END IF; " +
                        "   RETURN NEW; "+
                        "END; " +
                        "$$ LANGUAGE PLPGSQL; " +

                        "DROP TRIGGER IF EXISTS trig_set_sale_bool " +
                        "ON PUBLIC.product;" +

                        "CREATE TRIGGER trig_set_sale_bool " +
                        " BEFORE INSERT OR UPDATE " +
                        " ON PRODUCT " +
                        " FOR EACH ROW " +
                        " EXECUTE PROCEDURE set_sale_bool();";
         stmt.executeUpdate(sql);

         stmt.close();
      } catch ( Exception e ) {
         System.err.println( e.getClass().getName()+": "+ e.getMessage() );
         System.exit(0);
      }
      System.out.println("Создаётся таблица...");
      System.out.println();
   }
}
