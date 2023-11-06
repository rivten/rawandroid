package com.rivten.rawandroid;

import android.app.Activity;
import android.os.Bundle;

import android.util.Log;

public class StartActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.e(">>>", "hello world");
    }
}
