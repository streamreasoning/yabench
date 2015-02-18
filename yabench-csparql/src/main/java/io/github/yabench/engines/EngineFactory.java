package io.github.yabench.engines;

import java.lang.reflect.Modifier;
import java.util.Optional;
import java.util.Set;
import org.reflections.Reflections;

public class EngineFactory {

    public Engine create() throws Exception {
        Reflections reflections = new Reflections("io.github.yabench.engines");
        Set<Class<? extends Engine>> classes = reflections.getSubTypesOf(Engine.class);
        Optional<Class<? extends Engine>> r = classes.stream()
                .filter((clazz)-> !Modifier.isAbstract(clazz.getModifiers()))
                .findFirst();
        if (r.isPresent()) {
            return r.get().newInstance();
        } else {
            return null;
        }
    }
    
}
