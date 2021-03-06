package io.github.yabench.commons;

import java.util.Arrays;
import java.util.List;

public class TemporalGraph {

    private final List<TemporalTriple> triples;
    private final long time;

    public TemporalGraph(final List<TemporalTriple> triples) {
        if (!triples.isEmpty()) {
            this.triples = triples;
            this.time = triples.get(0).getTime();
        } else {
            throw new IllegalArgumentException();
        }
    }
    
    public TemporalGraph(final TemporalTriple[] triples) {
        if(triples.length > 0) {
            this.triples = Arrays.asList(triples);
            this.time = triples[0].getTime();
        } else {
            throw new IllegalArgumentException();
        }
    }
    
    public List<TemporalTriple> getTriples() {
        return triples;
    }

    public long getTime() {
        return time;
    }

}
