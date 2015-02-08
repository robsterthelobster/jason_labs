public class Assert{
    static void Assert(boolean b){
        if(!b)
            throw new RuntimeException("ERROR");
    }
}
