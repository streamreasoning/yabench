package io.github.yabench.engines;

import com.hp.hpl.jena.sparql.engine.binding.Binding;
import java.util.List;

public interface ResultListener {
    
    public void update(List<Binding> binding);
    
}
