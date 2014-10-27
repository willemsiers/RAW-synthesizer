using UnityEngine;
using System.Collections;

public interface IInstrument {
	string getName ();
	bool playNote (Vector2 pitch);
}
