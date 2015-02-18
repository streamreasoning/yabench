package io.github.yabench.engines;

import com.hp.hpl.jena.sparql.core.Var;
import com.hp.hpl.jena.sparql.engine.binding.Binding;
import java.io.IOException;
import java.io.Writer;
import java.util.Iterator;
import java.util.List;

public class ResultSerializer implements ResultListener {

    private static final String NEWLINE = "\n";
    private static final String TAB = "\t";
    private final Writer writer;
    private boolean initialized = false;
    private boolean firstResult = true;

    public ResultSerializer(Writer writer) {
        this.writer = writer;
    }

    public void initialize() throws IOException {
        if (!initialized) {
            writer.write(System.currentTimeMillis() + NEWLINE);
            initialized = true;
        }
    }

    @Override
    public void update(List<Binding> bindings) {
        try {
            if (firstResult) {
                Iterator<Var> vars = bindings.get(0).vars();
                while (vars.hasNext()) {
                    Var var = vars.next();
                    writer.write(var.getVarName() + TAB);
                }
                writer.write(NEWLINE);
                firstResult = false;
            }
            
            final long timestamp = System.currentTimeMillis();
            writeln(timestamp);
            
            for(Binding binding : bindings) {
                final Iterator<Var> vars = binding.vars();
                while(vars.hasNext()) {
                    final Var var  = vars.next();
                    writer.write(binding.get(var).toString(false) + TAB);
                }
                writer.write(NEWLINE);
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
    
    private void writeln(final Object string) throws IOException {
        writer.write(string + NEWLINE);
    }

}
